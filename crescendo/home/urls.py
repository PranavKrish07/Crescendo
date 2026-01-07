from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('start_roadmap/<int:quest_id>/', views.start_roadmap, name='start_roadmap'),
    path('roadmap/<int:progress_id>/', views.open_roadmap, name='open_roadmap'),
    path('<str:quest_name>/', views.openQuest, name='open_quest'),
    path('delete/<int:quest_id>/', views.delete_quest, name='delete_quest'),
]