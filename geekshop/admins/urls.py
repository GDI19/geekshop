from django.contrib import admin
from django.urls import path
from admins.views import index, admin_users, admin_users_create, admin_users_update, admin_users_delete
from admins.views import admin_category, admin_category_create, admin_category_update, admin_category_delete

from admins.views import product_create, products_read, product_update, product_delete
from mainapp.views import products


app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_users, name='admin_users'),
    path('users-create/', admin_users_create,name='admin_users_create'),
    path('users-update/<int:pk>', admin_users_update, name='admin_users_update'),
    path('users-delete/<int:pk>', admin_users_delete, name='admin_users_delete'),

    path('category/', admin_category, name='admin_category'),
    path('category/create/', admin_category_create, name='admin_category_create'),
    path('category-update/<int:pk>', admin_category_update, name='admin_category_update'),
    path('category-delete/<int:pk>', admin_category_delete, name='admin_category_delete'),

    path('products/read/', products_read, name='products_read'),
    path('products/create/category/<int:pk>/', product_create, name='product_create'),
    path('products/read/category/<int:pk>/', products, name='products'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
]


