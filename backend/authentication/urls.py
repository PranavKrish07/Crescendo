from django.urls import path
from .views import (
    SignupView, VerifyOTPView, LoginView,
    ForgotPasswordView, ResetPasswordView,
    GetScenesView, SubmitAwakeningView, MeView,
)

urlpatterns = [
    path('signup/',           SignupView.as_view()),
    path('verify-otp/',       VerifyOTPView.as_view()),
    path('login/',            LoginView.as_view()),
    path('forgot-password/',  ForgotPasswordView.as_view()),
    path('reset-password/',   ResetPasswordView.as_view()),

    # Awakening
    path('awakening/scenes/', GetScenesView.as_view()),
    path('awakening/submit/', SubmitAwakeningView.as_view()),

    # User profile
    path('me/',               MeView.as_view()),
]