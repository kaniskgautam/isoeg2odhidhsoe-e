
from django import template
from ..models import ImageUrl, Product

register = template.Library()


@register.filter
def index(indexable, i):
    try:
        return indexable[i]
    except:
        return []


@register.filter
def first(indexable):
    try:
        return indexable.first().url
    except:
        return []


@register.simple_tag
def get_image_url(product_id, *args, **kwargs):
    prod = Product.objects.get(id=product_id)
    img_url = ImageUrl.objects.filter(product=prod, primary=True)

    print("IMAGE URL", img_url, prod)

    if img_url:
        return img_url[0].url
    else:
        return "https://dummyimage.com/450x300/dee2e6/6c757d.jpg"


@register.simple_tag
def od_category(order):
    p = Product.objects.get(id=order.product)

    return p.category


@register.simple_tag
def od_code_url(order):
    p = Product.objects.get(id=order.product)

    return p.code_url


@register.simple_tag
def od_title(order):
    p = Product.objects.get(id=order.product)

    return p.title


@register.simple_tag
def od_price(order):
    p = Product.objects.get(id=order.product)

    return p.price

# register.filter('index', index)
