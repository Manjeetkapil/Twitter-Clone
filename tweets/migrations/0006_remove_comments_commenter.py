# Generated by Django 3.1.7 on 2021-05-04 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20210504_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='commenter',
        ),
    ]