from django.urls import path
# import basketapp.views as basketapp
from basketapp.views import basket_add, basket_remove

app_name = 'basketapp'


urlpatterns = [
    # path('', basketapp.basket, name='view' ),
    path('add/<int:id>/', basket_add, name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
