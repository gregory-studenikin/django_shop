from django.shortcuts import render

from .scraping import scraping_electric, ScrapingError


def fill_database(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping_electric()
        except ScrapingError as err:
            print(str(err))
            return render(request, 'shop/fill-products.html', {'message': str(err)})

    return render(request, 'shop/fill-products.html', {'message': None})


def productdetail(request):
    return render(request, 'shop/productdetail.html')


def products(request):
    return render(request, 'shop/products.html')


def shoppingcart(request):
    return render(request, 'shop/shoppingcart.html')
