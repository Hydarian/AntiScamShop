from django.contrib import admin
from .models import TheShop


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['name']

