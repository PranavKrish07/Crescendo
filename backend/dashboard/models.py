from django.db import models
from django.conf import settings
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    exp   = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    aura  = models.IntegerField(default=0)
    rank  = models.CharField(default='E', max_length=1)

    str_points = models.FloatField(default=0)
    end_points = models.FloatField(default=0)
    agi_points = models.FloatField(default=0)
    int_points = models.FloatField(default=0)
    cha_points = models.FloatField(default=0)
    wil_points = models.FloatField(default=0)

    streak = models.PositiveIntegerField(default=0)
    streak_freezes = models.PositiveIntegerField(default=2)
    last_checkin = models.DateField(null=True, blank=True)
    
    streak_breaks_this_month = models.PositiveIntegerField(default=0)
    last_streak_break_date = models.DateField(null=True, blank=True)

    days_at_aura_cap = models.PositiveIntegerField(default=0)
    ritual_lockout_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — Lv.{self.level}"

    @property
    def xp_threshold(self):
        """Returns max XP required for current level. Exponential formula."""
        return int(100 * (1.5 ** (self.level - 1)))
        
    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.xp_threshold:
            self.exp -= self.xp_threshold
            self.level += 1
        self.save()

    def get_aura_cap(self):
        caps = {'E': 900, 'D': 1600, 'C': 2500, 'B': 3200, 'A': 4200, 'S': 999999}
        return caps.get(self.rank, 900)

    def add_aura(self, amount):
        cap = self.get_aura_cap()
        self.aura += amount
        if self.aura > cap:
            self.aura = cap
        self.save(update_fields=['aura'])
        self.update_rank()

    def update_rank(self):
        # Only demotions happen automatically. Rank ups require a ritual.
        if self.aura < 900 and self.rank != 'E':
            self.rank = 'E'
        elif self.aura < 1600 and self.rank not in ['E', 'D']:
            self.rank = 'D'
        elif self.aura < 2500 and self.rank not in ['E', 'D', 'C']:
            self.rank = 'C'
        elif self.aura < 3200 and self.rank in ['A', 'S']:
            self.rank = 'B'
        elif self.aura < 4200 and self.rank == 'S':
            self.rank = 'A'
        self.save(update_fields=['rank'])

    def evaluate_streak(self):
        if not self.last_checkin:
            return
        
        today = timezone.now().date()
        days_passed = (today - self.last_checkin).days
        
        if days_passed > 1:
            missed_days = days_passed - 1
            if self.streak_freezes >= missed_days:
                self.streak_freezes -= missed_days
                self.last_checkin = today - timezone.timedelta(days=1)
                self.save(update_fields=['streak_freezes', 'last_checkin'])
            else:
                self.streak = 0
                self.streak_freezes = 0
                self.last_checkin = today - timezone.timedelta(days=1)
                
                # Monthly streak break logic
                if self.last_streak_break_date and self.last_streak_break_date.month != today.month:
                    self.streak_breaks_this_month = 0
                
                self.streak_breaks_this_month += 1
                self.last_streak_break_date = today
                
                if self.streak_breaks_this_month >= 5:
                    penalty_map = {'E': 45, 'D': 55, 'C': 70, 'B': 90, 'A': 120, 'S': 150}
                    penalty = penalty_map.get(self.rank, 45)
                    self.aura -= penalty
                    self.update_rank()
                
                self.save(update_fields=['streak', 'streak_freezes', 'last_checkin', 'streak_breaks_this_month', 'last_streak_break_date', 'aura', 'rank'])

    def check_in(self):
        self.evaluate_streak()
        today = timezone.now().date()
        if self.last_checkin != today:
            self.streak += 1
            self.last_checkin = today
            # Cap logic
            if self.aura >= self.get_aura_cap():
                self.days_at_aura_cap += 1
            else:
                self.days_at_aura_cap = 0
            self.save(update_fields=['streak', 'last_checkin', 'days_at_aura_cap'])


class Quest(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    STAT_CHOICES = [
        ('STR', 'Strength'),
        ('END', 'Endurance'),
        ('AGI', 'Agility'),
        ('INT', 'Intelligence'),
        ('CHA', 'Charisma'),
        ('WIL', 'Willpower'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stat = models.CharField(max_length=3, choices=STAT_CHOICES, null=True, blank=True)
    deadline = models.DateTimeField()
    is_daily = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='EASY')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_difficulty(self):
        count = self.subtasks.count()
        if count <= 6:
            self.difficulty = 'EASY'
        elif count <= 12:
            self.difficulty = 'MEDIUM'
        else:
            self.difficulty = 'HARD'
        self.save(update_fields=['difficulty'])

    def __str__(self):
        return f"{self.title} - {self.user.email}"

class SubTask(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='subtasks')
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{'x' if self.is_completed else ' '}] {self.description}"

class UserRitual(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rituals')
    target_rank = models.CharField(max_length=1) # D, C, B, A, S
    status = models.CharField(max_length=20, default='ACTIVE') # ACTIVE, COMPLETED, FAILED
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    requirements_state = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.email} - Ritual to {self.target_rank} ({self.status})"

class RoadmapTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stat = models.CharField(max_length=3, choices=Quest.STAT_CHOICES)
    difficulty = models.CharField(max_length=10, choices=Quest.DIFFICULTY_CHOICES, default='MEDIUM')
    tasks = models.JSONField(default=list) # List of strings representing tasks
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.stat} - {self.difficulty})"

class UserRoadmap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmaps')
    template = models.ForeignKey(RoadmapTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Quest.STATUS_CHOICES, default='PENDING')
    deadline = models.DateTimeField()
    progress = models.JSONField(default=list) # List of booleans corresponding to template.tasks
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.template.title} ({self.status})"