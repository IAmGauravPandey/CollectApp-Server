from django.urls import path

from . import views

urlpatterns = [
    path('create/', view=views.CreateSession.as_view()),
    path('join/', view=views.JoinSession.as_view()),
    path('list/', view=views.SessionList.as_view()),
    path('member/list/', view=views.SessionMember.as_view()),
]
