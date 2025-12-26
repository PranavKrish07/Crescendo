from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User_profile

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    return render(request, 'index.html')

@login_required
def home(request):
    user_profile = User_profile.objects.filter(user=request.user).first()
    if not user_profile or not user_profile.is_quiz_completed:
        return HttpResponseRedirect('/quiz/1/')
    return render(request, 'home.html', {'user_details': user_profile})