from django.urls import path
from mainapp.views import products, ProductDetail

app_name = 'mainapp'

urlpatterns = [
   path('', products, name='products'),
   # path('<int:pk>/', mainapp.products, name='category'),
   path('detail/<int:pk>/', ProductDetail.as_view(), name='detail' ),
]

