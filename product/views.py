from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template_name = 'product/index.html'
    return render(request, template_name)
