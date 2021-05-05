from django.contrib import admin
from django.urls import path, include
from tweets import views as tweets_view

urlpatterns = [
    path('newtweet/', tweets_view.newtweet, name='newtweet'),
    path('tweets/<slug:username>/', tweets_view.mytweets, name='mytweets'),
    path('tweets/<pk>', tweets_view.spetweet, name='tweetdetail'),
    path('mytweets/edit/<pk>', tweets_view.edittweet, name='edittweet'),
    path('tweet/likers', tweets_view.likers, name='likers'),
    path('', tweets_view.homepage, name='home'),
    path('like_unlike/', tweets_view.like_unlike, name='like_unlike'),
    path('retweet/', tweets_view.retweet, name='retweet'),
    path('comment/<pk>', tweets_view.newcomment, name='comment')
]
