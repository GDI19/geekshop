from datetime import timedelta

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


def get_activation_key_expired_date():
    return now() + timedelta(hours=48)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expired_date)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
