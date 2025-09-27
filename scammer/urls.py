from . import views
from django.urls import path
from . import views
app_name = 'scam'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('result', views.SearchResult.as_view(), name='result'),
    path('detail/<int:pk>/<slug:slug>', views.DetailShop.as_view(), name='detail'),
]