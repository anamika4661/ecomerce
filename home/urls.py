from django.contrib import admin
from django.urls import path
from .views import *

app_name = "home"
urlpatterns = [
    path('', HomeView.as_view(),name = 'home'),
    path('product/<slug>', ProductDetailView.as_view(), name='product'),
    path('search', searchview.as_view(), name='search'),
    path('category/<slug>', categoryview.as_view(), name='category'),
    path('signup', register,name = 'signup'),
    path('signin', signin,name = 'signin'),
    path('cart', viewcart.as_view(),name = 'cart'),
    path('add-to-cart/<slug>', cart1,name = 'add-to-cart'),
    path('delete-cart/<slug>', deletecart, name='delete-cart'),
    path('delete-single-cart/<slug>', cartminus, name='delete-single-cart'),
    path('brand/<name>', brandview.as_view(), name='brand'),
    path('contact', contactsave, name='contact'),
]
