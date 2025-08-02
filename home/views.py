from django.shortcuts import render
from .models import PhysicalStat, MentalStat, Class, Rank, Difficulty, Quiz
def landing(request):
    return render(request, 'index.html')

def home(request):
    physical = PhysicalStat.objects.all()
    mental = MentalStat.objects.all()
    classes = Class.objects.all()
    ranks = Rank.objects.all()
    difficulties = Difficulty.objects.all()
    user_quiz_class = request.session.get('quiz_class', None)


    return render(request, 'home.html', {'class':user_quiz_class, 'physical': physical, 'mental': mental, 'classes': classes, 'ranks': ranks, 'difficulties': difficulties})

def physicalstats(request):
    physical = PhysicalStat.objects.all()
    return render(request, 'physicalstats.html', {'physical': physical})

def mentalstats(request):
    mental = MentalStat.objects.all()
    return render(request, 'mentalstats.html', {'mental': mental})

def quiz(request):
    questions = Quiz.objects.all()
    if request.method == 'POST':
        # Initialize a dictionary to hold the score for each option
        scores = {
            'A': 0,
            'B': 0,
            'C': 0,
        }

        class_map = {
            'A': 'Knight',
            'B': 'Samurai',
            'C': 'Ninja'
        }
        
        for key, value in request.POST.items():
            if key.startswith('option'):
                if value in scores:
                    scores[value] += 1
        highest_option = max(scores, key=scores.get)
        final_class = class_map.get(highest_option, 'Undetermined') 
        request.session['quiz_class'] = final_class
        return render(request, 'results.html', {'final_class': final_class})



    return render(request, 'quiz.html', {'questions': questions})