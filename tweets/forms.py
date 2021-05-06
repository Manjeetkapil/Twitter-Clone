from django import forms
from django.forms import Textarea
from django.contrib.auth.models import User

from .models import Tweets


class newTweetform(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']
        widgets = {
            'tweet': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class editTweetform(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']
        widgets = {
            'tweet': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
