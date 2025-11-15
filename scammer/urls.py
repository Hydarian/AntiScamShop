from . import views
from django.urls import path
from . import views
app_name = 'scam'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('result', views.SearchResult.as_view(), name='result'),
    path('detail/<int:pk>/<slug:slug>', views.DetailShop.as_view(), name='detail'),
    path('like-shop', views.LikeShop.as_view(), name='like_shop'),
    path('dislike-shop', views.DisLikeShop.as_view(), name='dislike_shop'),
    path('login', views.Login.as_view(), name='login')

]