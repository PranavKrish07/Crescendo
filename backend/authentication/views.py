from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
from .serializers import *
from .awakening_data import SCENES, CLASSES
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
            
            try:
                send_mail(
                    'Verify your Crescendo account',
                    f'Your OTP is: {otp_code}\nIt expires in 10 minutes.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"SMTP Mail Delivery Error: {str(e)}")
                return Response({
                    'message': 'User registered, but failed to send verification email.',
                    'debug_error': str(e)
                }, status=status.HTTP_201_CREATED)

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
                return Response({
                    'message': 'Account verified.',
                    'tokens': tokens,
                    'name': user.name,
                    'awakening_done': user.awakening_done,
                })
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
                return Response({
                    'tokens': tokens,
                    'name': user.name,
                    'awakening_done': user.awakening_done,
                })
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                return Response({'error': 'No account found with that email.'}, status=status.HTTP_404_NOT_FOUND)
            otp_code = generate_otp()
            OTP.objects.create(user=user, code=otp_code, purpose='reset')
            send_mail(
                'Reset your Crescendo password',
                f'Your password reset OTP is: {otp_code}\nIt expires in 10 minutes.',
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            return Response({'message': 'OTP has been sent to your email.'})
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


#  AWAKENING ENDPOINTS

class GetScenesView(APIView):
    """GET /api/auth/awakening/scenes/ — serve scenes without stat scores."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clean_scenes = []
        for scene in SCENES:
            clean_scenes.append({
                "id": scene["id"],
                "label": scene["label"],
                "title": scene["title"],
                "narrative": scene["narrative"],
                "question": scene["question"],
                "choices": [{"text": c["text"]} for c in scene["choices"]],
            })
        return Response(clean_scenes)


def assign_class(scores):
    """Determine the character class from tallied stat scores."""
    sorted_stats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary   = sorted_stats[0][0]
    secondary = sorted_stats[1][0]
    third     = sorted_stats[2][0]

    # Exact match
    for c in CLASSES:
        if c["primary"] == primary and c["secondary"] == secondary:
            # Oracle/Sage tiebreak — same INT/CHA pair
            if c["name"] == "Oracle" and third == "WIL":
                continue
            if c["name"] == "Sage" and third == "AGI":
                continue
            return c

    for c in CLASSES:
        if c["primary"] == primary:
            return c

    return CLASSES[0]


class SubmitAwakeningView(APIView):
    """POST /api/auth/awakening/submit/ — score answers and save class."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.awakening_done:
            return Response({"error": "Awakening already completed."}, status=400)

        answers = request.data.get("answers", [])  # list of ints, one per scene
        if len(answers) != len(SCENES):
            return Response({"error": "Invalid answer count."}, status=400)

        scores = {"STR": 0, "END": 0, "AGI": 0, "INT": 0, "CHA": 0, "WIL": 0}
        for scene_idx, choice_idx in enumerate(answers):
            scene = SCENES[scene_idx]
            if choice_idx < 0 or choice_idx >= len(scene["choices"]):
                return Response({"error": "Invalid choice index."}, status=400)
            for stat, val in scene["choices"][choice_idx]["stats"].items():
                scores[stat] += val

        assigned = assign_class(scores)

        # Save to user
        user.char_class     = assigned["name"]
        user.archetype      = assigned["archetype"]
        user.awakening_done = True
        user.stat_str = scores["STR"]
        user.stat_end = scores["END"]
        user.stat_agi = scores["AGI"]
        user.stat_int = scores["INT"]
        user.stat_cha = scores["CHA"]
        user.stat_wil = scores["WIL"]
        user.save()

        

        return Response({
            "class":     assigned["name"],
            "archetype": assigned["archetype"],
            "primary":   assigned["primary"],
            "secondary": assigned["secondary"],
            "scores":    scores,
        })


class MeView(APIView):
    """GET /api/auth/me/ — return the current authenticated user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email":          user.email,
            "name":           user.name,
            "awakening_done": user.awakening_done,
            "char_class":     user.char_class,
            "archetype":      user.archetype,
            "scores": {
                "STR": user.stat_str,
                "END": user.stat_end,
                "AGI": user.stat_agi,
                "INT": user.stat_int,
                "CHA": user.stat_cha,
                "WIL": user.stat_wil,
            }
        })