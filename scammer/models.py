from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام فروشگاه')
