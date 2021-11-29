from django.urls import path
from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('processdonation/', views.processDonation, name='processdonation'),
    path('successdonation/<str:args>/',
         views.donateSuccess, name='successdonation'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product, name='product'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('getprime/', views.getPrime, name="get_prime"),
    path('settings/', views.settings, name='settings'),
]
