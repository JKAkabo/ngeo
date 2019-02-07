from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AddProductForm, AddToStockForm, EditUnitPriceForm, SaleForm
from .models import Stock


def index(request):
    template_name = 'product/index.html'
    return render(request, template_name)


def add_product(request):
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
