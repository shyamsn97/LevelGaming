# Generated by Django 2.0 on 2017-12-24 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelgaming', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/default_profile_pic.png', upload_to='avatars/'),
        ),
    ]
