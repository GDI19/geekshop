from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache

from .models import ProductCategory, Product
import json
import os

MODULE_DIR = os.path.dirname(__file__)

def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key,link_category)
        return link_category
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key,link_product)
        return link_product
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key,product)
        return product
    else:
        return Product.objects.get(id=pk)


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


# @cache_page(3600)
@never_cache
def products(request, id_category=None, page=1):
    # file_path = os.path.join(MODULE_DIR, 'fixtures/goods.json')

    context = {
        'title': 'GeekShop-Каталог',
    }

    if id_category:
        #products = Product.objects.filter(category_id=id_category).select_related('category')
        products = get_link_product().filter(category_id=id_category)
    else:
        # products = Product.objects.all().select_related('category')
        products = get_link_product()

    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    # context['products'] = json.load(open(file_path, encoding='utf-8'))
    context['products'] = products_paginator
    context['categories'] = get_link_category()
    return render(request, 'mainapp/products.html', context)


# def contact(request):
#    return render(request, 'mainapp/contact.html')


class ProductDetail(DetailView):
    """
    Контроллер ввода информации о товаре
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # product = self.get_object()
        context['product'] = get_product(self.kwargs.get("pk"))
        return context
