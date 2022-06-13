from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from django.urls import reverse, reverse_lazy
from mainapp.models import ProductCategory, Product
from admins.forms import ProductCategoryEditForm, UserAdminRegisterForm, UserAdminProfileForm, ProductEditForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mainapp.mixin import CustomDispatchMixin, BaseClassContextMixin, UserDispatchMixin

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


class UsersListViews(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновить пользователя'


class UserDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    success_url = reverse_lazy('admins:admin_users')

    # template_name = 'admins/admin-users-update-delete.html'
    # form_class = UserAdminProfileForm
    # title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    title = 'Админстрирование категорий товаров'


class CategoryCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admins:admin_category')
    title = 'Создание категории'


class CategoryUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admins:admin_category')
    title = 'Редактирование категории'


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    title = 'Товары'


class ProductCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admins:products_read')
    title = 'Товар/создание'


class ProductUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/product-update.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admins:products_read')
    title = 'Редактирование товара'


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    success_url = reverse_lazy('admins:products_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
    else:
        instance.product_set.update(is_active=False)


"""
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
               # 'category': category,
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
"""