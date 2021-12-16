from django.urls import path
# import basketapp.views as basketapp
from basketapp.views import basket_add, basket_remove, basket_edit

app_name = 'basketapp'


urlpatterns = [
    # path('', basketapp.basket, name='view' ),
    path('add/<int:id>/', basket_add, name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('edit/<int:id_basket>/<int:quantity>/', basket_edit, name='basket_edit')
]
