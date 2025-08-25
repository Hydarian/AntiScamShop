from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class TheShop(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام فروشگاه')
    author = models.ForeignKey(User, related_name='shops', verbose_name='نویسنده', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())

    def likes_count(self):
        return self.likes.who_liked.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]


class Like(models.Model):
    shop = models.ForeignKey(TheShop, related_name='likes', on_delete=models.CASCADE)
    who_liked = models.ForeignKey(User, related_name='users_like', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop


class DisLike(models.Model):
    shop = models.OneToOneField(TheShop, related_name='dislikes', on_delete=models.CASCADE)
    who_Disliked = models.ManyToManyField(User, related_name='users_dislike')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop
