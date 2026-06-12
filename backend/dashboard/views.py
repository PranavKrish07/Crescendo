from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Quest, SubTask, UserRitual, RoadmapTemplate, UserRoadmap
from .serializers import QuestSerializer
from .services import evaluate_expired_quests, process_quest_completion, evaluate_expired_roadmaps, get_roadmap_aura_reward
from . import class_modifiers

class ProfileView(APIView):
    """GET /api/dashboard/profile/ — return combined User + UserProfile data."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Auto-create profile if it doesn't exist
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Lazy evaluation for expired quests and streak
        evaluate_expired_quests(user)
        evaluate_expired_roadmaps(user)
        profile.evaluate_streak()

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
            "streak": profile.streak,
            "streak_freezes": profile.streak_freezes,
            "last_checkin": profile.last_checkin,
            "days_at_aura_cap": profile.days_at_aura_cap,
            "ritual_lockout_until": profile.ritual_lockout_until,
            "aura_cap": profile.get_aura_cap()
        })

class CheckInView(APIView):
    """POST /api/dashboard/checkin/ — record a daily check-in."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        profile.check_in()

        # Apply class check-in effects (e.g., Sage: 15% chance to restore 50 Aura)
        checkin_effects = class_modifiers.on_checkin_effects(request.user, profile)

        response_data = {
            'status': 'Checked in successfully.',
            'streak': profile.streak,
            'streak_freezes': profile.streak_freezes,
            'last_checkin': profile.last_checkin
        }
        if checkin_effects:
            response_data['class_effects'] = checkin_effects
        return Response(response_data)

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
        quest.deadline = timezone.now()
        quest.save()
        return Response({'status': 'Quest marked as daily and deadline updated to today.'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        quest = self.get_object()

        # Alchemist class gate: cannot complete unless all subtasks done
        allowed, error_msg = class_modifiers.can_complete_quest(request.user, quest)
        if not allowed:
            return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

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

class RitualViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_ritual = UserRitual.objects.filter(user=request.user, status='ACTIVE').first()
        if not active_ritual:
            return Response({'active': False})
        
        return Response({
            'active': True,
            'id': active_ritual.id,
            'target_rank': active_ritual.target_rank,
            'started_at': active_ritual.started_at,
            'expires_at': active_ritual.expires_at,
            'requirements_state': active_ritual.requirements_state
        })

    @action(detail=False, methods=['post'])
    def apply(self, request):
        profile = request.user.profile
        
        if profile.rank == 'S':
            return Response({'error': 'You are already at the maximum rank.'}, status=400)
            
        if profile.ritual_lockout_until and profile.ritual_lockout_until > timezone.now():
            return Response({'error': 'You are currently locked out of rituals.'}, status=400)

        # Days required mapping + class modifier (Knight: +2 days)
        days_required = {'E': 7, 'D': 10, 'C': 14, 'B': 21, 'A': 30}
        req_days = days_required.get(profile.rank, 7)
        req_days += class_modifiers.get_ritual_extra_days(request.user)

        # Aura cap check with class modifier (Phantom: +15% cap requirement)
        aura_cap_mult = class_modifiers.get_ritual_aura_cap_multiplier(request.user)
        effective_cap = int(profile.get_aura_cap() * aura_cap_mult)

        if profile.days_at_aura_cap < req_days:
            return Response({'error': f'You must hold your Aura cap for {req_days} days to apply.'}, status=400)

        if profile.aura < effective_cap:
            return Response({'error': f'Your Aura must reach {effective_cap} to attempt a ritual.'}, status=400)

        if UserRitual.objects.filter(user=request.user, status='ACTIVE').exists():
            return Response({'error': 'You already have an active ritual.'}, status=400)

        # Target rank logic
        target_map = {'E': 'D', 'D': 'C', 'C': 'B', 'B': 'A', 'A': 'S'}
        target_rank = target_map.get(profile.rank)

        # Create the ritual
        expires_at = timezone.now() + timezone.timedelta(days=req_days)
        ritual = UserRitual.objects.create(
            user=request.user,
            target_rank=target_rank,
            expires_at=expires_at,
            requirements_state={} # Initialize appropriately based on rank
        )
        
        return Response({
            'status': 'Ritual started',
            'expires_at': expires_at,
            'target_rank': target_rank
        })

class RoadmapTemplateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        templates = RoadmapTemplate.objects.all()
        # Filter HARD roadmaps if user rank is below B (i.e. E, D, C)
        profile = request.user.profile
        if profile.rank in ['E', 'D', 'C']:
            templates = templates.exclude(difficulty='HARD')
            
        data = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'stat': t.stat,
            'difficulty': t.difficulty,
            'tasks': t.tasks,
            'reward': 2 if t.difficulty == 'EASY' else (4 if t.difficulty == 'MEDIUM' else 6)
        } for t in templates]
        
        return Response(data)

class UserRoadmapViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active(self, request):
        roadmaps = UserRoadmap.objects.filter(user=request.user, status='PENDING')
        data = [{
            'id': r.id,
            'template_id': r.template.id,
            'title': r.template.title,
            'description': r.template.description,
            'stat': r.template.stat,
            'difficulty': r.template.difficulty,
            'tasks': r.template.tasks,
            'progress': r.progress,
            'deadline': r.deadline,
            'reward': 2 if r.template.difficulty == 'EASY' else (4 if r.template.difficulty == 'MEDIUM' else 6)
        } for r in roadmaps]
        return Response(data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        template_id = request.data.get('template_id')
        deadline = request.data.get('deadline')
        if not template_id or not deadline:
            return Response({'error': 'template_id and deadline required'}, status=400)
            
        try:
            template = RoadmapTemplate.objects.get(id=template_id)
        except RoadmapTemplate.DoesNotExist:
            return Response({'error': 'Template not found'}, status=404)
            
        # Ensure user doesn't already have this active
        if UserRoadmap.objects.filter(user=request.user, template=template, status='PENDING').exists():
            return Response({'error': 'You already have this roadmap active'}, status=400)
            
        # Rank-based capacity limits + class modifier (Ronin: -1 slot)
        active_count = UserRoadmap.objects.filter(user=request.user, status='PENDING').count()
        rank = request.user.profile.rank
        
        limit = 3
        if rank == 'A':
            limit = 4
        elif rank == 'S':
            limit = 9999  # unlimited
        
        limit += class_modifiers.get_roadmap_slot_modifier(request.user)
        limit = max(1, limit)  # Ensure at least 1 slot
            
        if active_count >= limit:
            return Response({'error': f'Your Rank ({rank}) only allows {limit} active roadmaps at a time.'}, status=400)
            
        progress = [False] * len(template.tasks)
        r = UserRoadmap.objects.create(
            user=request.user,
            template=template,
            deadline=deadline,
            progress=progress
        )
        return Response({'status': 'Registered successfully', 'id': r.id})

    @action(detail=True, methods=['post'])
    def toggle_task(self, request, pk=None):
        try:
            r = UserRoadmap.objects.get(id=pk, user=request.user)
        except UserRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=404)
            
        if r.status != 'PENDING':
            return Response({'error': 'Roadmap is not active'}, status=400)
            
        task_index = request.data.get('task_index')
        if task_index is None or task_index < 0 or task_index >= len(r.progress):
            return Response({'error': 'Invalid task index'}, status=400)
            
        r.progress[task_index] = not r.progress[task_index]
        
        # Check completion
        if all(r.progress):
            r.status = 'COMPLETED'
            r.completed_at = timezone.now()
            
            # Award Growth Points with class GP multipliers
            base_reward = 2 if r.template.difficulty == 'EASY' else (4 if r.template.difficulty == 'MEDIUM' else 6)
            profile = request.user.profile
            gp_multipliers = class_modifiers.get_roadmap_gp_multipliers(
                request.user, profile, r
            )
            stat_key = r.template.stat.upper()
            stat_field = f"{r.template.stat.lower()}_points"
            current_val = getattr(profile, stat_field, 0)
            multiplied_reward = base_reward * gp_multipliers.get(stat_key, 1.0)
            setattr(profile, stat_field, current_val + multiplied_reward)
            
            # Award Aura based on rank and difficulty
            aura_reward = get_roadmap_aura_reward(profile.rank, r.template.difficulty)
            profile.add_aura(aura_reward)
            
            # Award XP with class roadmap XP multiplier
            base_xp = 10
            xp_mult = class_modifiers.get_roadmap_xp_multiplier(request.user, profile)
            profile.add_exp(int(base_xp * xp_mult))
            
            profile.save()
            
        r.save()
        return Response({'status': 'Task toggled', 'progress': r.progress, 'completed': r.status == 'COMPLETED'})

    @action(detail=True, methods=['post'])
    def break_oath(self, request, pk=None):
        try:
            r = UserRoadmap.objects.get(id=pk, user=request.user)
            if r.status != 'PENDING':
                return Response({'error': 'Only active roadmaps can be broken'}, status=400)
                
            profile = request.user.profile

            # Ninja Buff 2 (Agile Pivot): 1 free roadmap abandon per month
            if class_modifiers.use_free_roadmap_abandon(request.user, profile):
                r.delete()
                return Response({'status': 'Oath broken. Ninja Agile Pivot — no Aura penalty this time.'})

            from .services import get_roadmap_aura_reward
            base_penalty = get_roadmap_aura_reward(profile.rank, r.template.difficulty)
            
            # Apply class failure multiplier (Paladin doubles penalty)
            failure_mult = class_modifiers.get_roadmap_failure_aura_multiplier(
                request.user, profile, r
            )
            penalty = int(base_penalty * failure_mult)
            
            profile.aura -= penalty
            profile.save()
            profile.update_rank()
            
            r.delete()
            return Response({'status': 'Oath broken. Aura penalty applied.', 'aura_penalty': penalty})
        except UserRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=404)
