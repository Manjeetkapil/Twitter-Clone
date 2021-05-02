from django.db import models
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import User


class Tweets(models.Model):
    tweeter = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=10000)
    tweet_time = models.DateTimeField(default=datetime.now, blank=True)
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


class Comments(models.Model):
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    comment_time = models.DateTimeField(default=datetime.now, blank=True)
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


class Likes(models.Model):
    tweet = models.OneToOneField(
        Tweets, on_delete=models.CASCADE, related_name='whotweeted')
    liker = models.ManyToManyField(User, related_name='liker', blank=True)
