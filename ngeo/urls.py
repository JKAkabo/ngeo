from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
]
