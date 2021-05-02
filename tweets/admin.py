from django.contrib import admin

from .models import Tweets, Likes
# Register your models here.
admin.site.register(Tweets)
admin.site.register(Likes)
