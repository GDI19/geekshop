from django.shortcuts import render
from .models import ProductCategory, Product
import json
import os

MODULE_DIR = os.path.dirname(__file__)


def main(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    # file_path = os.path.join(MODULE_DIR, 'fixtures/goods.json')
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {
        'title': 'GeekShop-Каталог',
        'products': products,
        'categories': categories,
    }

    # context['products'] = json.load(open(file_path, encoding='utf-8'))
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')
