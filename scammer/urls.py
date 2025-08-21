from . import views
from django.urls import path

app_name = 'scam'

urlpatterns = [
    path('', views.index, name='index'),
]