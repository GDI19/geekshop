from django.shortcuts import render

import json
import os

MODULE_DIR = os.path.dirname(__file__)

def main(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/goods.json')
    context = {
        'title': 'GeekShop-Каталог',
    }

    context['products'] = json.load(open(file_path, encoding='utf-8'))
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')

