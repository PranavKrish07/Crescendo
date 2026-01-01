from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('<str:quest_name>/', views.openQuest, name='open_quest'),
    path('delete/<int:quest_id>/', views.delete_quest, name='delete_quest'),
]