# Generated by Django 2.0 on 2017-12-26 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.TextField(blank=True, max_length=5000000000000)),
                ('followers', models.TextField(blank=True, max_length=5000000000000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(max_length=5000000000000)),
                ('username', models.TextField(default='', max_length=60000000)),
                ('description', models.TextField(default='', max_length=60000000)),
                ('title', models.TextField(default='', max_length=60000000)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
