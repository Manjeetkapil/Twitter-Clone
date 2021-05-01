from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Follower(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    follower = models.ManyToManyField(
        User, related_name='personfollower', blank=True)

    def __str__(self):
        return f'{self.person}'


class Following(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    following = models.ManyToManyField(
        User, related_name='personfollowing', blank=True)

    def __str__(self):
        return f'{self.person}'
