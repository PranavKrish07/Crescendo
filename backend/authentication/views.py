from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
from .serializers import *
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_code = generate_otp()
            OTP.objects.create(user=user, code=otp_code, purpose='verify')
            send_mail(
                'Verify your Crescendo account',
                f'Your OTP is: {otp_code}\nIt expires in 10 minutes.',
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                otp  = OTP.objects.filter(user=user, code=serializer.validated_data['otp'], purpose='verify', is_used=False).latest('created_at')
                if otp.is_expired():
                    return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
                otp.is_used = True
                otp.save()
                user.is_active = True
                user.save()
                tokens = get_tokens_for_user(user)
                return Response({'message': 'Account verified.', 'tokens': tokens})
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                if not user.check_password(serializer.validated_data['password']):
                    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
                if not user.is_active:
                    return Response({'error': 'Please verify your email first.'}, status=status.HTTP_403_FORBIDDEN)
                tokens = get_tokens_for_user(user)
                return Response({'tokens': tokens, 'name': user.name})
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                otp_code = generate_otp()
                OTP.objects.create(user=user, code=otp_code, purpose='reset')
                send_mail(
                    'Reset your Crescendo password',
                    f'Your password reset OTP is: {otp_code}\nIt expires in 10 minutes.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
            except User.DoesNotExist:
                pass  # silent — don't expose whether email exists
            return Response({'message': 'If that email exists, an OTP has been sent.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                otp  = OTP.objects.filter(user=user, code=serializer.validated_data['otp'], purpose='reset', is_used=False).latest('created_at')
                if otp.is_expired():
                    return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
                otp.is_used = True
                otp.save()
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password reset successful.'})
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)