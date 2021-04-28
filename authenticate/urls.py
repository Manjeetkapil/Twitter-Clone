from django.contrib import admin
from django.urls import path, include
from authenticate import views as authenticate_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', authenticate_views.register, name='register'),
    # path('login/', authenticate_views.Userlogin, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authenticate/logout.html'), name='logout'),
]
