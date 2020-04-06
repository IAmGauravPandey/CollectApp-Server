from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    path('create/',view=views.CreateSession.as_view()),
    path('join/',view=views.JoinSession.as_view()),
    path('list/',view=views.SessionList.as_view()),
    path('member/list/',view=views.SessionMember.as_view()),
]