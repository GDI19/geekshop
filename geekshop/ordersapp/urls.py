from django.urls import path

from ordersapp.views import OrderList, OrderDelete, OrderCreate, OrderDetail, OrderUpdate
from ordersapp.views import order_forming_complete, get_product_price

app_name = 'ordersapp'
urlpatterns = [

    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),

    path('product/<int:pk>/price/', get_product_price, name='product_price')
]