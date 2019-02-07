from django import forms

from .models import Product, Sale, Stock


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'active_ingredients',
            'expiry_date',
        ]
        widgets = {
            'expiry_date': forms.SelectDateWidget(years=['2019', '2020', '2021']),
        }


class AddToStockForm(forms.Form):
    new_stock = forms.IntegerField(min_value=0)


class EditUnitPriceForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['unit_price']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity']