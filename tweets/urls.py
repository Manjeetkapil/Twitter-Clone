from django.contrib import admin
from django.urls import path, include
from tweets import views as tweets_view

urlpatterns = [
    path('newtweet/', tweets_view.newtweet, name='newtweet'),
    path('mytweets/', tweets_view.mytweets, name='mytweets'),
    path('mytweets/<pk>', tweets_view.spetweet, name='tweetdetail'),
    path('mytweets/edit/<pk>', tweets_view.edittweet, name='edittweet')
]
