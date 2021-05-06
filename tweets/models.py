from django.db import models
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Tweets(models.Model):
    tweeter = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=10000)
    tweet_time = models.DateTimeField(default=datetime.now, blank=True)
    retweeted = models.ManyToManyField(
        User, related_name='retweeter', blank=True)
    likes = models.IntegerField(default=0)


class Comments(models.Model):
    main_tweet = models.OneToOneField(
        Tweets, on_delete=models.CASCADE, related_name='maintweet', default=None)
    your_tweet = models.ManyToManyField(
        Tweets, related_name='comment', blank=True, default=None)


class Commentsrel(models.Model):
    commented_tweet = models.ForeignKey(
        Tweets, on_delete=models.CASCADE, related_name="commentedtweet")
    parent_tweet = models.ForeignKey(
        Tweets, on_delete=models.CASCADE, blank=True)


class Likes(models.Model):
    tweet = models.OneToOneField(
        Tweets, on_delete=models.CASCADE, related_name='whotweeted')
    liker = models.ManyToManyField(User, related_name='liker', blank=True)
