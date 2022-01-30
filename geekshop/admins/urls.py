from django.contrib import admin
from django.urls import path
from admins.views import index

from admins.views import UsersListViews, UserCreateView, UserUpdateView, UserDeleteView
from admins.views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from admins.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UsersListViews.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),

    path('category/', CategoryListView.as_view(), name='admin_category'),
    path('category/create/', CategoryCreateView.as_view(), name='admin_category_create'),
    path('category-update/<int:pk>', CategoryUpdateView.as_view(), name='admin_category_update'),
    path('category-delete/<int:pk>', CategoryDeleteView.as_view(), name='admin_category_delete'),

    path('products/read/', ProductListView.as_view(), name='products_read'),
    path('products/create/category/', ProductCreateView.as_view(), name='product_create', ),
    # path('products/read/category/<int:pk>/', products, name='products'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]


