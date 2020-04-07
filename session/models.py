from django.contrib.auth.models import User
from django.db import models


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
        # TODO: it should return person's name

'''
TODO: create models Chat, Transaction, TransactionGroup
Implement  push notification type feature for new chat message such that 
is notified to all members using WebSockets
'''

