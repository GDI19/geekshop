from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from django.template.loader import render_to_string
from mainapp.models import Product


'''
@login_required()
def basket_add(request, id):
    user_select = request.user
    product = Product.objects.get(id=id) # get_object_or_404(Product, id=id)
    baskets = Basket.objects.filter(user=user_select, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #  «вернуться туда же, откуда пришли».
'''
@login_required()
def basket_add(request, id):
    if request.is_ajax():
        user_select = request.user
        product = Product.objects.get(id=id) # get_object_or_404(Product, id=id)
        baskets = Basket.objects.filter(user=user_select, product=product)

        if baskets:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(user=user_select, product=product, quantity=1)

        products = Product.objects.all()
        context = {'products':products}
        result = render_to_string('mainapp/includes/card.html', context)
        return JsonResponse({'result': result})

@login_required()
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #  «вернуться туда же, откуда пришли».

@login_required
def basket_edit(request, id_basket, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id_basket)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        content = {'baskets': baskets}
        result = render_to_string('basketapp/basket.html', content)
        return JsonResponse({'result': result})

