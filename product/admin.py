from django.contrib import admin
from .models import Product, Sale, Stock, GroupSale

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'active_ingredients']


class SaleInline(admin.TabularInline):
    model = Sale
    extra = 1
    autocomplete_fields = ['product']


class GroupSaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'purchase_time']
    inlines = [
        SaleInline,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(GroupSale, GroupSaleAdmin)
admin.site.register(Stock)