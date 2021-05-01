from django import forms

from django.contrib.auth.models import User

from .models import Tweets


class newTweetform(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']


class editTweetform(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']
