from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_unit_price/<uuid:stock_id>/', views.edit_unit_price, name='edit_unit_price'),
    path('add_to_stock/<uuid:stock_id>/', views.add_to_stock, name='add_to_stock'),
    path('add_sale/', views.add_sale, name='add_sale'),
]
