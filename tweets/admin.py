from django.contrib import admin

from .models import Tweets, Likes, Comments, Commentsrel
# Register your models here.
admin.site.register(Tweets)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Commentsrel)
