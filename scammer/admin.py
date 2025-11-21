from django.contrib import admin
from .models import TheShop, Image


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(TheShop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'shop', 'created']
