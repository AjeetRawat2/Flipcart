from django.contrib import admin
from django.urls import path
from flipcart import views

urlpatterns = [
    path('', views.index, name='home'),
    path('check',views.check,name='check'),
    path('cart',views.cart,name='cart'),
]