from django.contrib.auth.models import User
from django.db import models
from authapp.models import Profile


class Session(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='Membership')
    secret_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.session.name
        
    def sessionName(self):
        return self.session.name
    
    def personName(self):
        person_profile=Profile.objects.get(user=self.person)
        return person_profile.name


