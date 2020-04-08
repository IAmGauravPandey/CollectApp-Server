from random import randint

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from authapp.constants import *
from authapp.models import Profile


class Register(APIView):
    """  
    This class is for registration of user in authapp by sending a verification of phone.If user is already
    registered in authapp then it will display a message showing already registered.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def _create_user(self, user, password, name):
        otp = randint(1000, 9999)
        otp = 1234
        user.set_password(password)
        user.save()
        p = Profile.objects.get(user=user)
        p.otp = str(otp)
        p.name=str(name)
        p.save()
        Token.objects.get_or_create(user=user)
        return JsonResponse({
            'success': True,
            'message': OTP_SENT_MESSAGE
        })

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        phone = data['phone']
        password = data['password']
        if User.objects.filter(username=phone).exists():
            user = User.objects.get(username=phone)
            if user.is_active:
                return JsonResponse({
                    'success': False,
                    'message': USER_EXISTS_MESSAGE
                })
            return self._create_user(user, password, name)
        user = User.objects.create_user(username=phone, password=password)
        user.is_active = False
        user.save()
        return self._create_user(user, password, name)


class VerifyAccount(APIView):
    """ 
    This class is for verifying the phone of the user by entering the otp
    in the authapp.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data['phone']
        # TODO: Verify it is a phone number
        otp = data['otp']
        otp = str(otp)
        user = User.objects.get(username=phone)
        user_profile = Profile.objects.get(user=user)
        if user_profile.otp == otp:
            user.is_active = True
            user.save()
            token = Token.objects.get(user=user)
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': SUCCESSFUL_VERIFICATION_MESSAGE,
                'access_token': token.key
            })
        else:
            return JsonResponse({
                'success':False,
                'message':WRONG_OTP_MESSAGE
            })


class Login(APIView):
    """  
    This class is for logging users in the authapp.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data['phone']
        # TODO: Verify it is a phone number
        password = data['password']
        user = authenticate(username=phone, password=password)

        if user is None:
            return JsonResponse({
                'success': False,
                'message': AUTH_FAIL_MESSAGE,
                'access_token': None
            })
        token = Token.objects.get(user=user)
        login(request, user)
        return JsonResponse({
            'success': True,
            'message': SUCCESSFUL_LOGIN_MESSAGE,
            'access_token': token.key
        })


class ForgotPassword(APIView):
    """
    In case the user forgots its password then it sends a otp for 
    resetting the password.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data['phone']
        # TODO: Verify it is a phone number
        if User.objects.filter(username=phone).count() == 0:
            return JsonResponse({
                'success': False,
                'message': USER_NOT_FOUND_MESSAGE
            })
        otp = randint(1000, 9999)
        # OTP should be either 4 or 6  digits only
        otp = 1234
        user = User.objects.get(username=phone)
        user_profile = Profile.objects.get(user=user)
        user_profile.otp = otp
        user_profile.save()
        return JsonResponse({
            'success': True,
            'message': OTP_SENT_MESSAGE
        })


class ResetPassword(APIView):
    """  
    This class verifies the otp for resetting password and allow users to 
    set new password.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data['phone']
        # TODO: Verify it is a phone number
        new_password = data['password']
        otp = data['otp']
        otp = str(otp)
        user = User.objects.get(username=phone)
        up = Profile.objects.get(user=user)
        if up.otp == otp:
            user.set_password(new_password)
            user.save()
            token = Token.objects.get(user=user)
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': SUCCESSFUL_PASSWORD_RESET_MESSAGE,
                'access_token': token.key
            })
        else:
            return JsonResponse({
                'success': False,
                'message': WRONG_OTP_MESSAGE,
                # 'access_token':None
            })
