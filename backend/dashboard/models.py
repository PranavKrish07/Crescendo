from django.db import models
from django.conf import settings

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