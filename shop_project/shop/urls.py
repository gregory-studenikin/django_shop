from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('fill-database/', views.fill_database, name='fill_database'),
    path('productdetail/', views.productdetail, name='productdetail'),
    path('products/', views.products, name='products'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
]
