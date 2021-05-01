from django.contrib import admin

# Register your models here.
from .models import Follower, Following

admin.site.register(Follower)
admin.site.register(Following)
