from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.TextField(max_length=5000000000000, blank=True)
    followers = models.TextField(max_length=5000000000000, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Video(models.Model):
    link = models.TextField(max_length=5000000000000)
    username = models.TextField(max_length= 60000000,default="")
    description = models.TextField(max_length= 60000000,default="")
    title = models.TextField(max_length= 60000000,default="")