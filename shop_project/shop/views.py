from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import AddQuantityForm
from .scraping import scraping_electric, ScrapingError

from django.views.generic import ListView, DetailView, DeleteView

from .models import Product, Order, OrderItem


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


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('shoppingcart')
        else:
            pass
    return redirect('products')


@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/shoppingcart.html', context)


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/shoppingcart.html'
    success_url = reverse_lazy(cart_view)

    # Проверка доступа
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs
