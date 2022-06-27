from django.shortcuts import render

from .scraping import scraping_electric, ScrapingError

from django.views.generic import ListView, DetailView

from .models import Product


def fill_database(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping_electric()
        except ScrapingError as err:
            print(str(err))
            return render(request, 'shop/fill-products.html', {'message': str(err)})

    return render(request, 'shop/fill-products.html', {'message': None})


class ProductsListView(ListView):
    model = Product
    template_name = 'shop/products.html'

class ProductsDetailView(DetailView):
    model = Product
    template_name = 'shop/productdetail.html'
