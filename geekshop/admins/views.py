from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from django.urls import reverse

from admins.forms import ProductCategoryEditForm, UserAdminRegisterForm, UserAdminProfileForm, ProductEditForm

from mainapp.models import ProductCategory, Product




@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    error_mess = ''
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
        else:
            error_mess = form.errors

    else:
        form = UserAdminRegisterForm()
    context = {
        'title': 'Geekshop - Админ | Регистрация',
        'form': form,
        'error_mess': error_mess
    }
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, pk):
    user_select = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=user_select)
    context = {
        'title': 'Geekshop - Админ | Обновление',
        'form': form,
        'user_select': user_select
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()

    return HttpResponseRedirect(reverse('admins:admin_users'))


@user_passes_test(lambda u: u.is_superuser)
def admin_category(request):
    context = {
        'title': 'Админстрирование категорий товаров',
        'object_list': ProductCategory.objects.all(),
    }
    return render(request, 'admins/admin-category-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_create(request):
    error_mess = ''
    if request.method == 'POST':
        form = ProductCategoryEditForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_category'))
        else:
            error_mess = form.errors

    else:
        form = ProductCategoryEditForm()
    context = {
        'title': 'Создание категории',
        'form': form,
        'error_mess': error_mess
    }
    return render(request, 'admins/admin-category-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_update(request, pk):
    category_select = ProductCategory.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductCategoryEditForm(data=request.POST, instance=category_select, files=request.FILES)
        if form.is_valid():
            category_select.is_active = True
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_category'))
    else:
        form = ProductCategoryEditForm(instance=category_select)
    context = {
        'title': 'Редактирование категории',
        'form': form,
        'category_select': category_select
    }
    return render(request, 'admins/admin-category-update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_category_delete(request, pk):
    if request.method == 'POST':
        category = ProductCategory.objects.get(pk=pk)
        category.is_active = False
        category.save()

    return HttpResponseRedirect(reverse('admins:admin_category'))


def products_read(request):
    title = 'Товары'
    products = Product.objects.all()
    content = {'title': title,
               'object_list': products,
               'category_list': ProductCategory.objects.all(),
               }

    return render(request, 'admins/admin-product-read.html', content)


def product_create(request):
    title = 'Товар/создание'
    # category = get_object_or_404(ProductCategory, pk=pk)
    error_mess = ''

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admins:products_read'))
        else:
            error_mess = product_form.errors
    else:
        product_form = ProductEditForm()

    content = {'title': title,
               'product_form': product_form,
               #'category': category,
               'error_mess': error_mess,
               }

    return render(request, 'admins/admin-product-create.html', content)


def product_update(request, pk):
    title = 'Редактирование товара'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, files=request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_product.is_active = True
            edit_form.save()
            return HttpResponseRedirect(reverse('admins:products_read'))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title,
               'update_form': edit_form,
               'category': edit_product.category,
               'pk': pk,
               }

    return render(request, 'admins/product-update.html', content)


def product_delete(request, pk):
    title = 'Удаление товара'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admins:products_read'))

    content = {'title': title, 'product_to_delete': product}

    return render(request, 'admins/admin-product-read.html', content)
