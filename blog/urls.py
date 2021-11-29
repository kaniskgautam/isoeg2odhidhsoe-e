from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('view/<slug:slug>/', views.view, name='blog_view'),
]
