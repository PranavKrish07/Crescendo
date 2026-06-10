from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileView, QuestViewSet, CheckInView, RitualViewSet, RoadmapTemplateViewSet, UserRoadmapViewSet

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')
router.register(r'rituals', RitualViewSet, basename='ritual')
router.register(r'roadmaps/templates', RoadmapTemplateViewSet, basename='roadmap-template')
router.register(r'roadmaps/user', UserRoadmapViewSet, basename='user-roadmap')

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('checkin/', CheckInView.as_view()),
    path('', include(router.urls)),
]
