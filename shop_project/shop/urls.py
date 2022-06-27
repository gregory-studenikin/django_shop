from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('fill-database/', views.fill_database, name='fill_database'),
    path('detail/<int:pk>/', views.ProductsDetailView.as_view(), name='productdetail'),
    path('products/', views.ProductsListView.as_view(), name='products'),
    path('shoppingcart/', TemplateView.as_view(template_name='shop/shoppingcart.html'), name='shoppingcart'),
]
