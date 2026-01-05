from django.urls import path
from . import views

urlpatterns = [
    path("takequiz/", views.take_quiz, name="take_quiz"),
    path("<int:pk>/", views.quiz, name="quiz"),
    path("result/", views.quiz_result, name="quiz_result"),
]