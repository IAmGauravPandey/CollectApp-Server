from django.urls import path

from . import views

urlpatterns = [
    path('group/create/',view=views.CreateTransactionGroup.as_view()),
    path('group/list/',view=views.TransactionGroupList.as_view()),
    path('create/',view=views.TransactionManager.as_view()),
    path('list/session/group/',view=views.TransactionListBySessionGroup.as_view()),
    path('list/session/',view=views.TransactionListBySession.as_view()),
]