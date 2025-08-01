from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('physicalstats/', views.physicalstats, name='physicalstats'),
    path('mentalstats/', views.mentalstats, name='mentalstats'),
    path('quiz/', views.quiz, name='quiz'),

]