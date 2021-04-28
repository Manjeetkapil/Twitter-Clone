from django.contrib import admin
from django.urls import path, include
from uprofile import views as profile_view

urlpatterns = [
    path('profile/', profile_view.profile, name='profile'),
    path('', profile_view.homepage, name='home')
]
