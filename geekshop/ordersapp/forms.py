from django import forms
from ordersapp.models import Order, OrderItem

from mainapp.models import Product


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):
        super(OrderItemsForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.active_items().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
