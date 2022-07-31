from django.test.client import Client
from django.core.management import call_command
from django.conf import settings
from django.test import TestCase

from authapp.models import User
from mainapp.models import Product
from ordersapp.models import Order, OrderItem
from basketapp.models import Basket

class TestOrdersapp(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.user = User.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains132')


    def test_order_listview(self):
        self.client.login(username='tarantino', password='geekbrains132')
        response = self.client.get('/orders/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.status_code, 200)

    def test_order_create(self):
        self.client.login(username='tarantino', password='geekbrains132')
        response1 = self.client.get('/auth/login/')
        self.assertEqual(response1.status_code, 200)
        self.assertFalse(response1.context['user'].is_anonymous)

        # неудачная попытка протестировать работу в заказах
        # добавим товар из базы с pk=20
        # response2 = self.client.post("/basket/add/20/", **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        # #self.assertFalse(response2.context['user'].is_anonymous)
        # response3 = self.client.get('/orders/create/')
        # print('response3', response3)

        # baskets = Basket.objects.filter(id=1)
        # basket = baskets.first()
        # print('basket', basket)

        # response4 = self.client.post('/orders/create/')
        # print('response4', response4)
        # #print('basket', str(response3.context['orderitems']))
        # #print(response3.context['object_list'])
#
        # order_item_quantity = OrderItem.objects.filter(pk=1)
        # order_item_1 = order_item_quantity.first()
        # print(str(order_item_1[0]))