from django.contrib.auth.models import User
from django.db import models
from session.models import Session

class TransactionGroup(models.Model):
    session=models.ForeignKey(Session,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    created_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    collector=models.ForeignKey(User,on_delete=models.CASCADE)
    group=models.ForeignKey(TransactionGroup,on_delete=models.CASCADE)
    date_of_payment=models.DateTimeField(auto_now=True)
    amount=models.CharField(max_length=100)
    payer_name=models.CharField(max_length=100)
    payer_phone=models.CharField(max_length=100)

    def __str__(self):
        return self.group.name