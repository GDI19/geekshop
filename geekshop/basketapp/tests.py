from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from mainapp.models import Product, ProductCategory
from authapp.models import User
from basketapp.models import Basket

class Test_Basket_views(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')

        # category = ProductCategory.objects.create(name="Джинсы")
        # self.product_1 = Product.objects.create(id=1, name="Деним", category=category, price=1999.5, quantity=10)
        # self.product_2 = Product.objects.create(id=2, name="Слим фит", category=category, price=2998.1, quantity=20, is_active=False)
        # self.product_3 = Product.objects.create(id=3, name="Клёш", category=category, price=2599.0, quantity=15)

        self.client = Client()
        self.user = User.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains132')

    def testing_basket(self):
        self.client.login(username='tarantino', password='geekbrains132')
        # логинимся
        response = self.client.get('/auth/login/')
        print(f'login response {response}')
        self.assertEqual(response.status_code, 200)
        # пустая корзина
        self.assertEqual(list(response.context['baskets']), [])
        # добавим товар из базы с pk=20
        self.client.post("/basket/add/20/", **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})

        response = self.client.get('/products/')
        product_in_basket = '<QuerySet [<Basket: Корзина для tarantino | Продукт Синяя куртка The North Face>]>'
        # print('response is: ', response.context['basket'])
        self.assertEqual(str(response.context['baskets']), product_in_basket)

        # проверяем сколько осталось товара на складе
        for rest_quantity in Product.objects.filter(pk=20):
            print('rest_quantity ', rest_quantity.quantity)
            self.assertEqual(rest_quantity.quantity, 99)

        # добавляем и снова проверяем сколько осталось товара на складе
        self.client.post("/basket/add/20/", **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        for rest_quantity in Product.objects.filter(pk=20):
            print('rest_quantity ', rest_quantity.quantity)
            self.assertEqual(rest_quantity.quantity, 98)

        # проверяем basket_edit views
        self.client.post('/basket/edit/1/5/', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        # print(response)
        # проверка кол-ва товара после редактирования
        baskets = Basket.objects.filter(id=1)
        basket = baskets.first()
        print('basket.quantity', basket.quantity)
        self.assertEqual(basket.quantity, 5)

        # проверяем сколько осталось товара на складе
        for rest_quantity in Product.objects.filter(pk=20):
            # print('rest_quantity ', rest_quantity.quantity)
            self.assertEqual(rest_quantity.quantity, 95)

        # удаляем и проверяем кол-во товара в корзине и на складе
        self.client.post('/basket/remove/1/', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        response = self.client.get('/products/')

        self.assertEqual(list(response.context['baskets']), [])
        for rest_quantity in Product.objects.filter(pk=20):
            print('rest_quantity ', rest_quantity.quantity)
            self.assertEqual(rest_quantity.quantity, 100)