from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User_profile, List
from .forms import ListForm

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    
    return render(request, 'index.html')

def calculate_threshold(level):
    return int(100 * (level ** 2))

def calculate_rank(trophies):
    if trophies >= 5000:
        return 'S'
    elif trophies >= 3500:
        return 'A'
    elif trophies >= 2200:
        return 'B'
    elif trophies >= 1200:
        return 'C'
    elif trophies >= 500:
        return 'D'
    else:
        return 'E'

@login_required
def home(request):
    user_profile = User_profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        listForm = ListForm(request.POST)
        if listForm.is_valid():
            new_list = listForm.save(commit=False)
            new_list.user = request.user
            new_list.save()
            return HttpResponseRedirect('/home/')
    else:
        listform = ListForm()
    if not user_profile or not user_profile.is_quiz_completed:
        return HttpResponseRedirect('/quiz/1/')
    
    current_level_threshold = calculate_threshold(user_profile.level)
    previous_level_threshold = calculate_threshold(user_profile.level - 1)
    #Maximum xp of  the current level
    level_range = current_level_threshold - previous_level_threshold
    # How much XP they have gained SINCE the last level
    xp_progress = user_profile.xp - previous_level_threshold
    xp_to_gain = level_range - xp_progress
    # trophies ranges
    

    Quests = List.objects.filter(user=request.user, is_completed=False)
    completed_quests = List.objects.filter(user=request.user, is_completed=True)

    #Ranks - Mental Stats
    int_rank = calculate_rank(user_profile.INT_trophies)
    per_rank = calculate_rank(user_profile.PER_trophies)
    wil_rank = calculate_rank(user_profile.WIL_trophies)
    cha_rank = calculate_rank(user_profile.CHA_trophies)

    #Ranks - Physical Stats
    str_rank = calculate_rank(user_profile.STR_trophies)
    agi_rank = calculate_rank(user_profile.AGI_trophies)
    vit_rank = calculate_rank(user_profile.VIT_trophies)
    end_rank = calculate_rank(user_profile.END_trophies)
    
    # Mental Stats List for template loop
    mental_stats = [
        {'name': 'Intelligence', 'rank': int_rank, 'trophies': user_profile.INT_trophies},
        {'name': 'Perception', 'rank': per_rank, 'trophies': user_profile.PER_trophies},
        {'name': 'Willpower', 'rank': wil_rank, 'trophies': user_profile.WIL_trophies},
        {'name': 'Charisma', 'rank': cha_rank, 'trophies': user_profile.CHA_trophies},
    ]
    
    # Physical Stats List for template loop
    physical_stats = [
        {'name': 'Strength', 'rank': str_rank, 'trophies': user_profile.STR_trophies},
        {'name': 'Agility', 'rank': agi_rank, 'trophies': user_profile.AGI_trophies},
        {'name': 'Vitality', 'rank': vit_rank, 'trophies': user_profile.VIT_trophies},
        {'name': 'Endurance', 'rank': end_rank, 'trophies': user_profile.END_trophies},
    ]
    
    return render(request, 'home.html', {'user_details': user_profile,
                                         'level_range': level_range, 
                                         'xp_progress': xp_progress, 
                                         'xp_to_gain': xp_to_gain, 
                                         'Quests': Quests, 
                                         'completed_quests': completed_quests, 
                                         'listform': listform,
                                         'mental_stats': mental_stats,
                                         'physical_stats': physical_stats})
