from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User_profile

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    
    return render(request, 'index.html')

def calculate_threshold(level):
    return int(100 * (level ** 2))

@login_required
def home(request):
    user_profile = User_profile.objects.filter(user=request.user).first()
    if not user_profile or not user_profile.is_quiz_completed:
        return HttpResponseRedirect('/quiz/1/')
    
    current_level_threshold = calculate_threshold(user_profile.level)
    previous_level_threshold = calculate_threshold(user_profile.level - 1)
    #Maximum xp of  the current level
    level_range = current_level_threshold - previous_level_threshold
    # How much XP they have gained SINCE the last level
    xp_progress = user_profile.xp - previous_level_threshold
    xp_to_gain = level_range - xp_progress
    return render(request, 'home.html', {'user_details': user_profile, 'level_range': level_range, 'xp_progress': xp_progress, 'xp_to_gain': xp_to_gain})