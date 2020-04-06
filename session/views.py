from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from session.models import *
from app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView,View
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.utils.dateparse import parse_datetime
from random import randint
import json
import random
import string
import datetime

class CreateSession(APIView):

    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def post(self,request,*args,**kwargs):
        data=request.data
        
        sessionName=data['sessionName']
        N=7
        user=request.user
        sessionToken=''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
        session=Session.objects.create(name=sessionName,secret_code=sessionToken,created_by=user.id)
        
        member=Membership.objects.create(person=user,session=session)
        member.is_admin=True
        member.save()
        user_profile=Profile.objects.get(user=user)
        return JsonResponse({
            'success':True,
            'message':'Club creates Successfully',
            'data':{
                'sessionId':session.id,
                'sessionName':sessionName,
                'sessionToken':sessionToken,
                'createdOn':member.date_joined.strftime('%d %B %Y'),
                'createdBy':user_profile.name,
                'createdById':user.id,
            }
        })

class JoinSession(APIView):

    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def post(self,request,*args,**kwargs):
        data=request.data
        sessionToken=data['sessionToken']
        sessionId=data['sessionId']
        session=Session.objects.get(id=sessionId)
        code=session.secret_code
        print(code)
        if str(code)==str(sessionToken):
            user=request.user
            member=Membership.objects.create(person=user,session=session)
            return JsonResponse({
                'message':'Joined the session Successfully.',
                'success':True
            })
        return JsonResponse({
            'message':'Incorrect SessionToken',
            'success':False
        })

class SessionList(APIView):

    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        sessionlist=[]
        for session in Session.objects.all():
            user=User.objects.get(id=session.created_by)
            profile=Profile.objects.get(user=user)
            sessionlist.append({
                'sessionId':session.id,
                'sessionName':session.name,
                'createdOn':session.created_at.strftime('%d %B %Y'),
                'createdBy':profile.name,
                'createdById':user.id
            })
        return JsonResponse({
            'message':'Session List Sent Successfully',
            'success':True,
            'data':sessionlist
        })

class SessionMember(APIView):

    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        sessionId=request.GET.get('sessionId')
        memberlist=[]
        session=Session.objects.get(id=sessionId)
        members=list(Membership.objects.filter(session=session).values())
        for member in members:
            user=User.objects.get(id=member['person_id'])
            profile=Profile.objects.get(user=user)
            memberlist.append({
                'userId':user.id,
                'userName':profile.name,
                'phone':user.username,
                'joinedOn':member['date_joined'].strftime('%d %B %Y'),
            })
        return JsonResponse({
            'success':True,
            'message':'Members list sent',
            'data':memberlist,
        })