from django.utils.functional import cached_property

from django.conf import settings
from django.db import models

# from authapp.models import User
from mainapp.models import Product

"""
class BasketQuerySet(models.QuerySet):
    # В Django работа с QuerySet возможна через менеджер модели.
   def delete(self, *args, **kwargs):
       for object in self:
           object.product.quantity += object.quantity
           object.product.save()
       super(BasketQuerySet, self).delete(*args, **kwargs)
"""


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    # objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def sum(self):
       return self.quantity * self.product.price

    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity

"""
    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)
"""






