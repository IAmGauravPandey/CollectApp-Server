from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class Session(models.Model):
    name=models.CharField(max_length=100)
    members=models.ManyToManyField(User,through='Membership')
    secret_code=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.IntegerField(default=1)
    def __str__(self):
        return self.name

class Membership(models.Model):
    person=models.ForeignKey(User,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,on_delete=models.CASCADE)
    date_joined=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.session.name
