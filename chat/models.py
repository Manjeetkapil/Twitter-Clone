from django.db import models

# Create your models here.


class Room(models.Model):
    key = models.IntegerField()
    message = models.TextField()
