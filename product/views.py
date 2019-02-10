from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AddProductForm, AddToStockForm, EditUnitPriceForm, SaleForm
from .models import Stock


def index(request):
    """
    Displays the total total stock and stock value from the model :model:`product.Stock`.

    **Template**
    :template:`product/index.html`
    """
    template_name = 'product/index.html'
    return render(request, template_name)


def add_product(request):
    """
    Displays a form that allows the addition of a product

    **Context**
        `` **GET** ``
        :form: A Form class for adding products
    
    **Template**
    :template:`product/add_product.html`
    """
    template_name = 'product/add_product.html'
    form = AddProductForm

    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            product = form.save()
        return redirect('product:edit_unit_price', stock_id=product.stock.id)
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)


def edit_unit_price(request, stock_id):
    """
    Displays a form that allows users to edit the the unit price of a product

    **Context**
        `` **GET** ``
        :form: A Form class for editting a the unit price of a product

    **Template**
    :template:`product/edit_unit_price.html`
    """
    template_name = 'product/edit_unit_price.html'
    stock = Stock.objects.get(id=stock_id)
    form = EditUnitPriceForm

    if request.method == 'POST':
        form = form(data=request.POST, instance=stock)
        if form.is_valid():
            form.save()
        return redirect('product:add_to_stock', stock_id=stock_id)
    else:
        context = {
            'form': form(instance=stock),
        }
        return render(request, template_name, context)

def add_to_stock(request, stock_id):
    """
    Displays a form that allows user to add to a a product's stock

    **Context**
        `` **GET** ``
        :form: A Form class for adding to stock

    **Template**
    :template:`product/add_to_stock.html`
    """
    template_name = 'product/add_to_stock.html'
    stock = Stock.objects.get(id=stock_id)
    form = AddToStockForm

    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            new_stock = form.cleaned_data['new_stock']
            stock.total_stock += new_stock
            stock.save()
        return redirect('product:add_to_stock', stock_id=stock_id)
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)


def add_sale(request):
    template_name = 'product/add_sale.html'
    form = SaleForm

    if request.method == 'POST':
        pass
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)
