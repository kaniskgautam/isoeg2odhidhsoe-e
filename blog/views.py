from django.shortcuts import render
from .models import Post
# Create your views here.


def index(request):

    posts = Post.objects.filter(status=1).order_by('-created_on')

    return render(request, 'blog/index.html', {'posts': posts})


def view(request, slug):

    blog = Post.objects.get(slug=slug)

    return render(request, 'blog/view.html', {'blog': blog})
