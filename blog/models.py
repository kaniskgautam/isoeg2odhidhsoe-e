from django.db import models
from django.contrib.auth.models import User
from mykode.settings import *

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    cover_image = models.CharField(
        max_length=300, default="https://dummyimage.com/450x300/dee2e6/6c757d.jpg")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
