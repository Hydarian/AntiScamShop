from . import views
from django.urls import path
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'scam'

urlpatterns = [

    path('', views.Index.as_view(), name='index'),
    path('result', views.SearchResult.as_view(), name='result'),
    path('detail/<int:pk>/<slug:slug>', views.DetailShop.as_view(), name='detail'),
    path('like-shop', views.LikeShop.as_view(), name='like_shop'),
    path('dislike-shop', views.DisLikeShop.as_view(), name='dislike_shop'),
    path('login', views.Login.as_view(), name='login'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('logout', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('create-post', views.CreatePost.as_view(), name='create_post'),
    path('edit-post/<int:pk>/<slug:slug>/', views.EditPost.as_view(), name='edit_post'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path("change-password/", auth_views.PasswordChangeView.as_view(template_name="registration/change-password.html", success_url=reverse_lazy('scam:change_password_done')), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='change_password_done'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('password-reset/', views.ResetPassword.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_confirm.html', success_url=reverse_lazy('scam:password_reset_complete'))
         ,name='reset_password_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'), name='password_reset_complete'),

]

