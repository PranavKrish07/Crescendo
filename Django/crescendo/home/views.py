from django.shortcuts import render
from .models import PhysicalStat, MentalStat
def landing(request):
    return render(request, 'index.html')

def home(request):
    physical = PhysicalStat.objects.all()
    mental = MentalStat.objects.all()
    return render(request, 'home.html', {'physical': physical, 'mental': mental})

def stats(request):
    physical = PhysicalStat.objects.all()
    return render(request, 'physicalstats.html', {'physical': physical})