from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView,View
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from random import randint
import json


class Register(APIView):
    """  
    This class is for registration of user in app by sending a verification of phone.If user is already 
    registered in app then it will display a message showing already registered.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        data=request.data
        name=data['name']
        phone=data['phone']
        password=data['password']
        if User.objects.filter(username=phone).count()!=0:
            user=User.objects.get(username=phone)
            if user.is_active:
                return JsonResponse({
                    'success':False,
                    'message':'User Already exist'
                })
            otp=randint(999,999999)
            otp=1234
            user.set_password(password)
            user.save()
            p=Profile.objects.get(user=user)
            p.name=name
            p.otp=str(otp)
            p.save()
            return JsonResponse({
                'success':True,
                'message':'User registered.Otp Send successfully'
            })
        user=User.objects.create_user(username=phone,password=password)
        user.is_active=False
        user.save()
        otp=randint(999,999999)
        otp=1234
        p=Profile.objects.get(user=user)
        p.name=name
        p.otp=str(otp)
        p.save()
        token=Token.objects.create(user=user)
        return JsonResponse({
            'success':True,
            'message':'User registered .Otp send successfully.'
        })
        
class VerifyAccount(APIView):
    """ 
    This class is for verifying the phone of the user by entering the otp
    in the app.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        data=request.data
        phone=data['phone']
        otp=data['otp']
        otp=str(otp)
        user=User.objects.get(username=phone)
        up=Profile.objects.get(user=user)
        if up.otp == otp:
            user.is_active = True
            user.save()
            token=Token.objects.get(user=user)
            login(request,user)
            return JsonResponse({
                'success':True,
                'message':'Verified Successfully',
                'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':'Wrong Otp',
                'access_token':None
            })

class Login(APIView):
    """  
    This class is for logging users in the app.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        data=request.data
        phone=data['phone']
        password=data['password']
        user=authenticate(username=phone,password=password)

        if user is None:
            return JsonResponse({
                'success':False,
                'message':'Authentication Failed',
                'access_token':None
            })
        token=Token.objects.get(user=user)
        login(request,user)
        return JsonResponse({
            'success':True,
            'message':'Logged In Successfully.',
            'access_token':token.key
        })

class ForgotPassword(APIView):
    """
    In case the user forgots its password then it sends a otp for 
    resetting the password.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        data=request.data
        phone=data['phone']
        if User.objects.filter(username=phone).count()==0:
            return JsonResponse({
                'success':False,
                'message':'User not exist'
            })
        otp=randint(999,999999)
        otp=1234
        user=User.objects.get(username=phone)
        up=Profile.objects.get(user=user)
        up.otp=otp
        name=up.name
        up.save()
        return JsonResponse({
            'success':True,
            'message':'Otp Send Successfully'
        })

class ResetPassword(APIView):
    """  
    This class verifies the otp for resetting password and allow users to 
    set new password.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        data=request.data
        phone=data['phone']
        new_password=data['password']
        otp=data['otp']
        otp=str(otp)
        user=User.objects.get(username=phone)
        up=Profile.objects.get(user=user)
        if up.otp == otp:
            user.set_password(new_password)
            user.save()
            token=Token.objects.get(user=user)
            login(request,user)
            return JsonResponse({
                'success':True,
                'message':'Reset Successful',
                'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':'Wrong Otp',
                #'access_token':None
            })