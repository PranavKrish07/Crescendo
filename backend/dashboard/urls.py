from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileView, QuestViewSet

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('', include(router.urls)),
]
