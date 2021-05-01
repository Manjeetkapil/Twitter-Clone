# Generated by Django 3.1.7 on 2021-05-01 20:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0006_auto_20210501_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='personfollower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='following',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='personfollowing', to=settings.AUTH_USER_MODEL),
        ),
    ]
