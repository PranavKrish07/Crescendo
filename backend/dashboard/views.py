from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Quest, SubTask
from .serializers import QuestSerializer
from .services import evaluate_daily_quests, process_quest_completion

class ProfileView(APIView):
    """GET /api/dashboard/profile/ — return combined User + UserProfile data."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Auto-create profile if it doesn't exist
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Lazy evaluation for expired daily quests
        evaluate_daily_quests(user)

        # Refresh profile to get updated aura after evaluation
        profile.refresh_from_db()

        return Response({
            # From User model
            "email":          user.email,
            "name":           user.name,
            "awakening_done": user.awakening_done,
            "char_class":     user.char_class,
            "archetype":      user.archetype,
            "scores": {
                "STR": user.stat_str,
                "END": user.stat_end,
                "AGI": user.stat_agi,
                "INT": user.stat_int,
                "CHA": user.stat_cha,
                "WIL": user.stat_wil,
            },
            # From UserProfile model
            "exp":   profile.exp,
            "max_exp": profile.xp_threshold,
            "level": profile.level,
            "aura":  profile.aura,
            "rank":  profile.rank,
            "growth_points": {
                "STR": profile.str_points,
                "END": profile.end_points,
                "AGI": profile.agi_points,
                "INT": profile.int_points,
                "CHA": profile.cha_points,
                "WIL": profile.wil_points,
            },
        })

class QuestViewSet(viewsets.ModelViewSet):
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quest.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        subtasks_data = request.data.pop('subtasks', [])
        
        # Validate deadline is required and not empty
        if not request.data.get('deadline'):
            return Response({'error': 'Deadline is mandatory.'}, status=status.HTTP_400_BAD_REQUEST)

        quest = Quest.objects.create(user=request.user, **request.data)
        
        for st in subtasks_data:
            if st.get('description'):
                SubTask.objects.create(quest=quest, description=st['description'])
        
        quest.calculate_difficulty()
        
        serializer = self.get_serializer(quest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def set_daily(self, request, pk=None):
        quest = self.get_object()
        quest.is_daily = True
        quest.save()
        return Response({'status': 'Quest marked as daily.'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        quest = self.get_object()
        process_quest_completion(quest)
        return Response({'status': 'Quest completed, rewards granted.'})
        
    @action(detail=False, methods=['post'], url_path=r'subtask/(?P<subtask_id>\d+)/toggle')
    def toggle_subtask(self, request, subtask_id=None):
        try:
            subtask = SubTask.objects.get(id=subtask_id, quest__user=request.user)
            subtask.is_completed = not subtask.is_completed
            subtask.save()
            
            # Check if all subtasks are completed, and if so, complete the quest automatically.
            quest = subtask.quest
            if quest.status == 'PENDING' and quest.subtasks.count() > 0:
                if not quest.subtasks.filter(is_completed=False).exists():
                    process_quest_completion(quest)
                    return Response({'status': 'Subtask toggled. Quest completed!', 'is_completed': subtask.is_completed, 'quest_completed': True})

            return Response({'status': 'Subtask toggled.', 'is_completed': subtask.is_completed, 'quest_completed': False})
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found.'}, status=404)

    @action(detail=True, methods=['post'])
    def add_subtask(self, request, pk=None):
        quest = self.get_object()
        if quest.status != 'PENDING':
            return Response({'error': 'Cannot add task to a completed or failed quest.'}, status=400)
        
        description = request.data.get('description')
        if not description:
            return Response({'error': 'Description is required.'}, status=400)
            
        SubTask.objects.create(quest=quest, description=description)
        quest.calculate_difficulty()
        return Response({'status': 'Subtask added and difficulty recalculated.'})

    @action(detail=False, methods=['delete'], url_path=r'subtask/(?P<subtask_id>\d+)')
    def delete_subtask(self, request, subtask_id=None):
        try:
            subtask = SubTask.objects.get(id=subtask_id, quest__user=request.user)
            quest = subtask.quest
            if quest.status != 'PENDING':
                return Response({'error': 'Cannot modify a completed or failed quest.'}, status=400)
                
            subtask.delete()
            quest.calculate_difficulty()
            return Response({'status': 'Subtask deleted and difficulty recalculated.'})
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found.'}, status=404)
