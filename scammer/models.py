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
    description = models.TextField(verbose_name='توضیحات')
    like = models.ManyToManyField(User, blank=True,  related_name='likes', verbose_name='لایک ها')
    dislike = models.ManyToManyField(User,  blank=True, related_name='dislikes', verbose_name='دیس لایک ها')
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


class Comment(models.Model):
    shop = models.ForeignKey(TheShop, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
