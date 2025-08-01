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

    return render(request, 'home.html', {'physical': physical, 'mental': mental, 'classes': classes, 'ranks': ranks, 'difficulties': difficulties})

def physicalstats(request):
    physical = PhysicalStat.objects.all()
    return render(request, 'physicalstats.html', {'physical': physical})

def mentalstats(request):
    mental = MentalStat.objects.all()
    return render(request, 'mentalstats.html', {'mental': mental})

def quiz(request):
    questions = Quiz.objects.all()
    return render(request, 'quiz.html', {'questions': questions})