from django.contrib import admin
from .models import TheShop, Image, Like, Dislike


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class DislikeInline(admin.TabularInline):
    model = Dislike
    extra = 0


@admin.register(TheShop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['name']
    inlines = [ImageInline, DislikeInline, LikeInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'shop', 'created']
