from . import views
from django.urls import path
from .views import Index, SearchResult
app_name = 'scam'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('result', SearchResult.as_view(), name='result'),
]