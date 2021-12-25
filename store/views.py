from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from .models import *
from blog.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  login, logout
from django.urls import reverse
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from mykode.settings import RAZORPAY_KEY, RAZORPAY_ID
from django.contrib.auth.decorators import login_required
import razorpay
from django.db.models import Q

# Create your views here.

# stripe.api_key = "sk_test_51IiCCKSFgQr5XVKDDKxHsGOsRT1im9e1M8KumJvagXSSvQzxeD7ojGEh3G3PdXTPc7VzkukPiRRIn6vBdud4UnN300Mvf0zixY"
client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_KEY))


@login_required(login_url="/signin")
def dashboard(request):

    orders = Order.objects.filter(
        customer=Customer.objects.get(id=request.user.id), complete=True)

    return render(request, 'store/account/dashboard.html', {"orders": orders})


@login_required(login_url="/signin")
def settings(request):

    if request.method == "POST" and request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if user.email != request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
            messages.success("Successfully updated Email")

    return render(request, 'store/account/settings.html')


@login_required(login_url="/signin")
def getPrime(request):

    return render(request, 'store/getprime.html')


def page_404(request):

    return render(request, 'store/404.html')


def index(request):

    query = request.GET.get('query')  # Search query
    if query:
        print("QUERY", query)
        query = query.replace(' ', '+')
        return redirect(reverse('products') + "?query=" + query)

    if not request.user.is_authenticated:
        recent_blogs = Post.objects.all().order_by('-id')[:3]
        return render(request, 'store/index.html', {"recent_blogs": recent_blogs})

    # customer = request.user.customer
    # print("CUSTOMER : ", customer)

    # products = Product.objects.filter(category="python")
    # n = 4
    # l = []
    # for i in range(0, len(products), n):
    #     l.append(products[i:i + n])

    # print(l)
    # params = {
    #     "python_products": l
    # }
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds,
              "products": Product.objects.filter(category="python")[:4]}

    return render(request, 'store/home.html', params)


def about(request):
    return render(request, 'store/about.html')


def signin(request):

    if request.method == "POST":
        # print(request)
        username = request.POST['username']
        password = request.POST['password']

        # print("USERNAME : " , username)
        # print("PASSWORD : " , password)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("signin")

    return render(request, 'store/signin.html')


def signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not email:
            messages.error(request, "Please Enter a valid Email")
            return redirect('signup')

        if len(username) < 3:
            messages.error(request, "User name is too short")
            return redirect('signup')

        if len(password) < 5:
            messages.error(request, "Password is too short.")
            return redirect('signup')

        if not any(i.isdigit() for i in str(password)):
            messages.error(
                request, "Password does not contain any Number. Please include a number")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already Exists")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        customer = Customer(user=myuser, name=username, email=email)
        customer.save()
        messages.success(request, "Your ACCOUNT has been successfully created")
        return redirect('index')

    return render(request, 'store/signup.html')


@login_required(login_url="/signin")
def signout(request):  # DONE
    logout(request)

    messages.success(request, "Successfully logged out")

    return redirect('index')


def donate(request):

    return render(request, 'store/donation.html')


@csrf_exempt
def processDonation(request):

    return redirect(reverse('successdonation', args=[0]))


def donateSuccess(request, args):  # DONE
    amount = args
    return render(request, 'store/donationSuccess.html', {"amount": amount})


@csrf_exempt
def productBuy(request, id):

    product = Product.objects.get(id=id)
    price = product.price * 100
    order_currency = 'INR'

    payment = client.order.create(
        {'amount': price,
            'currency': order_currency,
            'payment_capture': '1',
         })

    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)

            print(request.POST)
            if result is None:
                try:
                    client.payment.capture(payment_id, price)

                    order = Order.objects.get(order_id=razorpay_order_id)

                    order.complete = True
                    order.payment_id = payment_id

                    order.save()

                    return render(request, 'paymentsuccess.html')
                except:
                    return render(request, 'paymentfailure.html')
            else:
                render(request, 'paymentfailure.html')
        except:
            return HttpResponseBadRequest()

    return render(request, 'store/productBuy.html', {"product": product, "price": price, "order_id": payment['id']})


@csrf_exempt
def product(request, id):

    product = Product.objects.get(id=id)
    price = product.price * 100
    order_currency = 'USD'

    payment = client.order.create(
        {'amount': price,
            'currency': order_currency,
            'payment_capture': '0',
         })

    image_urls = ImageUrl.objects.filter(product=product)
    related_products = Product.objects.filter(
        category=product.category).filter(~Q(id=product.id))[:4]

    can_download = False
    if request.user.is_authenticated:
        order_bought = Order.objects.filter(
            customer=Customer.objects.get(id=request.user.id), product=product.id)

        for pp in order_bought:
            if str(pp.product) == str(product.id):
                can_download = True
    else:
        messages.warning(request, "Please ", extra_tags="login")

    if request.method == "POST":
        print("Product")
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)

            if result == None:
                try:
                    client.payment.capture(payment_id, price)

                    order = Order(customer=request.user.customer, product=product.id,
                                  complete=True, order_id=razorpay_order_id, payment_id=payment_id)

                    order.save()

                    return render(request, 'store/paymentsuccess.html', {"product": product})
                except Exception as e:
                    print(e)
                    return render(request, 'store/paymentfailure.html', {"product": product})
            else:
                render(request, 'store/paymentfailure.html',
                       {"product": product})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()

    return render(request, 'store/product.html', {"can_download": can_download, "product": product, "price": price, "order_id": payment['id'], "image_urls": image_urls, "related_products": related_products})


def products(request):  # DONE FOR NOW

    products = Product.objects.all()  # Getting all Products available

    query = request.GET.get('query')  # Search query
    filter_by = request.GET.get('filter_by')  # Filter / Order Products

    # Search Code
    if query:
        print(query)
        products = products.filter(title__icontains=query)
    if filter_by:
        if filter_by == "price_hl":  # High to Low Price
            products = products.order_by('-price')
        elif filter_by == "price_lh":  # Low to High Price
            products = products.order_by('price')
        elif filter_by == "popular":  # Popular products
            products = products.order_by('-rating')

    # Paginator Code
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'store/products.html', {"products": products})


def contact(request):  # DONE

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if (len(subject) < 5):
            messages.error(request, "The Message is too short .")
            return redirect('contact')
        if (len(message) < 10):
            messages.error(request, "Message is too short.")
            return redirect('contact')

        my_contact = Message(name=name, email=email,
                             subject=subject, message=message)
        my_contact.save()

        messages.success(
            request, "Message Sucessfully Sent ! You will get response on your given email id in 2 or 3 business days.")

    return render(request, 'store/contact.html')
