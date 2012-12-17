from django.db.models.signals import pre_delete, pre_save, post_save, post_syncdb

from EventApp.models import *
from django.contrib.auth.models import User

from django.contrib.auth import models as auth_app, get_user_model




def auto_create_superuser(*args, **kwargs):

    user = User.objects.create_superuser("akfreas", "akfreas@gmail.com", "AppValveWin")
    user.save()

post_syncdb.connect(auto_create_superuser,
    sender=auth_app, dispatch_uid="django.contrib.auth.management.create_superuser")
