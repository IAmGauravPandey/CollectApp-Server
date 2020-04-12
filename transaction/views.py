from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from authapp.models import Profile
from session.models import *
from transaction.models import *

class CreateTransactionGroup(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data=request.data
        session_id=data['sessionId']
        group_name=data['groupName']
        session=Session.objects.get(id=session_id)
        group=TransactionGroup.objects.create(name=group_name,session=session)

        return JsonResponse({
            'success':True,
            'message':'Transaction Group creates successfully',
            'groupId':group.id,
            'groupName':group.name,
            'createdOn':group.created_on.strftime("%b %d, %Y %I:%M %p"),
        })

class TransactionGroupList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        session_id=request.GET.get('sessionId')
        group_list=[]
        session=Session.objects.get(id=session_id)
        groups=list(TransactionGroup.objects.filter(session=session).values())
        for group in groups:
            group_list.append({
                'groupId':group['id'],
                'groupName':group['name'],
                'createdOn':group['created_on'].strftime("%b %d, %Y %I:%M %p"),
            })
        return JsonResponse({
            'success':True,
            'message':'Group list sent',
            'data':group_list,
        })


class TransactionManager(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data=request.data
        payer_name=data['payerName']
        amount=data['amount']
        payer_phone=data['payerPhone']
        payment_date=data['paymentDate']
        group_id=data['groupId']
        session_id=data['sessionId']
        collector_id=data['collectorId']
        collector=User.objects.get(id=collector_id)
        collector_profile=Profile.objects.get(user=collector)
        group=TransactionGroup.objects.get(id=group_id)
        transaction=Transaction.objects.create(collector=collector,group=group,
        date_of_payment=payment_date,amount=amount,payer_name=payer_name,
        payer_phone=payer_phone
        )
        return JsonResponse({
            'success':True,
            'message':'Transaction data saved',
            'data':{
                'payerName':payer_name,
                'payerPhone':payer_phone,
                'amount':amount,
                'paidOn':payment_date,
                'collectedById':collector.id,
                'collectedBy':collector_profile.name,
            }
        })

class TransactionListBySessionGroup(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        session_id=request.GET.get('sessionId')
        group_id=request.GET.get('groupId')
        group=TransactionGroup.objects.get(id=group_id)
        transactions=list(Transaction.objects.filter(group=group).values())
        transaction_list=[]
        for transaction in transactions:
            collector=User.objects.get(id=transaction['collector_id'])
            collector_profile=Profile.objects.get(user=collector)
            transaction_list.append({
                'payerName':transaction['payer_name'],
                'payerPhone':transaction['payer_phone'],
                'amount':transaction['amount'],
                'paidOn':transaction['date_of_payment'].strftime("%b %d, %Y %I:%M %p"),
                'collectedById':collector.id,
                'collectedBy':collector_profile.name
            })
        return JsonResponse({
            'success':True,
            'message':'Transaction list sent',
            'data':transaction_list,
        })

class TransactionListBySession(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        session_id=request.GET.get('sessionId')
        session=Session.objects.get(id=session_id)
        groups=list(TransactionGroup.objects.filter(session=session).values())
        transactions=[]
        for group in groups:
            for tl in list(Transaction.objects.filter(id=group['id']).values()):
                transactions.append(tl)
        print(transactions)
        transaction_list=[]
        for transaction in transactions:
            collector=User.objects.get(id=transaction['collector_id'])
            collector_profile=Profile.objects.get(user=collector)
            transaction_list.append({
                'payerName':transaction['payer_name'],
                'payerPhone':transaction['payer_phone'],
                'amount':transaction['amount'],
                'paidOn':transaction['date_of_payment'].strftime("%b %d, %Y %I:%M %p"),
                'collectedById':collector.id,
                'collectedBy':collector_profile.name
            })
        return JsonResponse({
            'success':True,
            'message':'Transaction list sent',
            'data':transaction_list,
        })