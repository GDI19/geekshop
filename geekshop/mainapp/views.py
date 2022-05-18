from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView

from .models import ProductCategory, Product
import json
import os

MODULE_DIR = os.path.dirname(__file__)


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request, id_category=None, page=1):
    # file_path = os.path.join(MODULE_DIR, 'fixtures/goods.json')
    if id_category:
        products = Product.objects.filter(category_id=id_category, is_active=True, category__is_active=True).select_related('category')
    else:
        products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)


    categories = ProductCategory.objects.filter(is_active=True)
    context = {
        'title': 'GeekShop-Каталог',
        'products': products_paginator,
        'categories': categories,
    }

    # context['products'] = json.load(open(file_path, encoding='utf-8'))
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')


class ProductDetail(DetailView):
    """
    Контроллер ввода информации о товаре
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs).select_related('category')
        product = self.get_object()
        context['product'] = product
        return context
