from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User_profile, List, Task
from .forms import ListForm, TaskForm
from django.forms import modelformset_factory

checkboxformset = modelformset_factory(Task, fields=('is_completed',), extra=0)

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

    if user_profile.xp >= calculate_threshold(user_profile.level):
        user_profile.level += 1
        user_profile.save()
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

@login_required
def delete_quest(request, quest_id):
    quest = List.objects.filter(id=quest_id, user=request.user).first()
    if not quest:
        raise Http404("Quest not found")
    quest.delete()
    return HttpResponseRedirect('/home/')

@login_required
def openQuest(request, quest_name):
    quest = List.objects.filter(name=quest_name, user=request.user).first()
    if not quest:
        raise Http404("Quest not found")
    quest_tasks = Task.objects.filter(list=quest)
    completed_tasks = quest_tasks.filter(is_completed=True).count()
    total_tasks = quest_tasks.count()

    if total_tasks <= 5:
        xp_gain = 10
        difficulty = 'Simple'
    elif total_tasks <= 15:
        xp_gain = 25
        difficulty = 'Easy'
    elif total_tasks <= 30:
        xp_gain = 45
        difficulty = 'Medium'
    elif total_tasks <= 50:
        xp_gain = 70
        difficulty = 'Hard'
    else:
        xp_gain = 100
        difficulty = 'Extreme'

    if quest.difficulty != difficulty:
        quest.difficulty = difficulty
        quest.save()

    if total_tasks > 0 and completed_tasks == total_tasks and not quest.is_completed:
        quest.is_completed = True
        quest.save()
        profile = request.user.user_profile
        profile.xp += xp_gain
        profile.save()
    #forms
    taskForm = TaskForm()
    formset = checkboxformset(queryset=quest_tasks)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_task':
            form = TaskForm(request.POST)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.list = quest
                new_task.save()
                return HttpResponseRedirect(f"/{quest.name}/")
        elif action == 'update_tasks':
            formset = checkboxformset(request.POST, queryset=quest_tasks)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(f"/{quest.name}/")
        
    return render(request, 'openQuest.html', {'quest_tasks': quest_tasks, 'quest_name': quest.name, 'taskForm':taskForm, 'formset': formset, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks, 'difficulty': difficulty})