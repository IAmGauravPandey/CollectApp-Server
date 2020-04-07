from django.urls import path

from . import views

urlpatterns = [
    path('signup/', view=views.Register.as_view()),
    path('verify_otp/', view=views.VerifyAccount.as_view()),
    path('signin/', view=views.Login.as_view()),
    path('forgot_password/', view=views.ForgotPassword.as_view()),
    path('reset_password/', view=views.ResetPassword.as_view()),
]
