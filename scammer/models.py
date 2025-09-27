from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify



# Create your models here.
class TheShop(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام فروشگاه')
    author = models.ForeignKey(User, related_name='shops', verbose_name='نویسنده', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    created = models.DateTimeField(default=timezone.now())

    def likes_count(self):
        return User.objects.filter(users_like__shop=self).count()

    def dislikes_count(self):
        return User.objects.filter(users_dislike__shop=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:  # فقط اگه slug خالیه
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'


class Like(models.Model):
    shop = models.ForeignKey(TheShop, related_name='likes', on_delete=models.CASCADE)
    who_liked = models.ManyToManyField(User, related_name='users_like', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop


class Dislike(models.Model):
    shop = models.OneToOneField(TheShop, related_name='dislikes', on_delete=models.CASCADE)
    who_Disliked = models.ManyToManyField(User, related_name='users_dislike', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop


class Image(models.Model):
    shop = models.ForeignKey(TheShop, on_delete=models.CASCADE, related_name='images')
    img_file = models.ImageField(upload_to='post_images/', blank=True, null=True)
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='موضوع')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'None'


