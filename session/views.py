import random
import string

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from authapp.models import Profile
from session.models import *


class CreateSession(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data

        sessionName = data['sessionName']
        N = 7
        user = request.user
        # Use lowercase variables in python
        sessionToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        session = Session.objects.create(name=sessionName, secret_code=sessionToken, created_by=user.id)

        member = Membership.objects.create(person=user, session=session)
        member.is_admin = True
        member.save()
        user_profile = Profile.objects.get(user=user)
        return JsonResponse({
            'success': True,
            'message': 'Session created Successfully',  # Use constant file for string responses
            'data': {
                'sessionId': session.id,
                'sessionName': sessionName,
                'sessionToken': sessionToken,
                'createdOn': member.date_joined.strftime("%b %d, %Y %I:%M %p"),
                'createdBy': user_profile.name,
                'createdById': user.id,
            }
        })


class JoinSession(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data
        session_token = data['sessionToken']
        session_id = data['sessionId']
        session = Session.objects.get(id=session_id)
        code = session.secret_code
        print(code)
        if str(code) == str(session_token):
            user = request.user
            member = Membership.objects.create(person=user, session=session)
            return JsonResponse({
                'message': 'Session joined successfully.',
                'success': True
            })
        return JsonResponse({
            'message': 'Incorrect Session Token',
            'success': False
        })


class SessionList(APIView):
    # TODO: Create and Implement permission.IsMember
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        session_list = []
        for session in Session.objects.all():
            user = User.objects.get(id=session.created_by)
            profile = Profile.objects.get(user=user)
            session_list.append({
                'sessionId': session.id,
                'sessionName': session.name,
                'createdOn': session.created_at.strftime("%b %d, %Y %I:%M %p"),
                'createdBy': profile.name,
                'createdById': user.id
            })
        return JsonResponse({
            'message': 'Session list received successfully',
            'success': True,
            'data': session_list
        })


class SessionMember(APIView):
    # TODO: Create and Implement permission.IsMember
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('sessionId')
        member_list = []
        session = Session.objects.get(id=session_id)
        members = list(Membership.objects.filter(session=session).values())
        for member in members:
            user = User.objects.get(id=member['person_id'])
            profile = Profile.objects.get(user=user)
            member_list.append({
                'userId': user.id,
                'userName': profile.name,
                'phone': user.username,
                'joinedOn': member['date_joined'].strftime("%b %d, %Y %I:%M %p"),
            })
        return JsonResponse({
            'success': True,
            'message': 'Member list received successfully',
            'data': member_list,
        })
