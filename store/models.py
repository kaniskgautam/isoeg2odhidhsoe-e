from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import translation
# from .settings import *
# Create your models here.


# class User(AbstractUser):
#     description = models.CharField(max_length=500, default='')
#     is_email_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email
from mykode.settings import *


class Customer(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, related_name='customers_user', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name


CATEGORIES = (
    ("Python", "Python"),
    ("Others", "Others"),
    ("C++", "C++"),
)


class Product(models.Model):
    # image_url = models.CharField(
    #     max_length=500, default="https://dummyimage.com/450x300/dee2e6/6c757d.jpg")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.FloatField()
    rating = models.FloatField()
    # created_by = models.CharField(max_length=201)
    made_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store_product', default=1)
    category = models.CharField(
        choices=CATEGORIES, max_length=100, default="others")
    code_url = models.CharField(
        max_length=500, default="https://firebasestorage.googleapis.com/v0/b/kode-36169.appspot.com/o/productCodeFiles%2F256b5ee0-afbe-441d-bdcb-2b4e7efc47af.zip?alt=media&token=58e7473f-1e8a-46d6-b74a-a3d374f33410")
    reviewed = models.BooleanField(default=False)
    sales = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.reviewed}"


class ImageUrl(models.Model):
    url = models.CharField(
        max_length=500, default="https://dummyimage.com/450x300/dee2e6/6c757d.jpg")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)


class Tag(models.Model):
    user = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    broad_category = models.CharField(max_length=200, default="others")


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,  on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=200, default="")
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=200, null=True)
    payment_id = models.CharField(max_length=200, null=True, default=None)

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    message = models.TextField()
    email = models.EmailField()
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject}'
