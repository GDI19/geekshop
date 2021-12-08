import json, os
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
# from django.contrib.auth.models import User
from authapp.models import User

JSON_PATH = 'mainapp/fixtures'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name+'.json'), mode='r', encoding='utf-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()


        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] =_category
            new_category = Product(**prod)
            new_category.save()

        # Создаем суперпользователя при помощи менеджера модели
        super_user = User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=37)


