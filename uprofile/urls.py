from django.contrib import admin
from django.urls import path, include, re_path
from uprofile import views as profile_view

urlpatterns = [
    path('profile/', profile_view.profile, name='profile'),
    path('profile/<slug:username>/',
         profile_view.viewprofile, name='viewprofile'),
    path('profile/follower/<slug:username>/',
         profile_view.viewfollower, name='follower'),
    path('profile/following/<slug:username>/',
         profile_view.viewfollowing, name='following'),
    path('profiles/<slug:username>/',
         profile_view.follow_unfollow, name='follow_unfollow')
]
