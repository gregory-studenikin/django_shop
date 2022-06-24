from django.shortcuts import render


def index(request):
    return render(request, template_name='index.html')


def about(request):
    return render(request, template_name='about.html')


def checkout(request):
    return render(request, template_name='checkout.html')


def productdetail(request):
    return render(request, template_name='productdetail.html')


def products(request):
    return render(request, template_name='products.html')


def shoppingcart(request):
    return render(request, template_name='shoppingcart.html')
