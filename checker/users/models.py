from django.contrib.auth.models import AbstractUser
from django.db import models


class WhitelistedUser(AbstractUser):
    username = models.BigIntegerField(
        verbose_name='Телеграмм ID',
        unique=True
    )
    telegramm_username = models.CharField(
        verbose_name='Пользователь',
        max_length=255,
        unique=False,
    )


class BlacListUser(models.Model):
    telegram_id = models.BigIntegerField(
        verbose_name='Телеграмм ID',
        unique=True
    )