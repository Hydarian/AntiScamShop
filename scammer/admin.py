from django.contrib import admin
from .models import TheShop


# Register your models here.
@admin.register(TheShop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['name']

