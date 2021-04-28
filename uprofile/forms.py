from django import forms

from django.contrib.auth.models import User

from .models import Profile


class profileUpdateform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'intro', 'age']


class userUpdateform(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
