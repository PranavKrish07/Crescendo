from django.db import models
from authentication.models import User

class User_profile(models.Model):
    #basicinfo
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_class = models.CharField(max_length=20, blank=True, null=True)
    is_quiz_completed = models.BooleanField(default=False)

    #Global Levelling - this level will go based completing tasks and todo
    level = models.PositiveBigIntegerField(default=1)
    xp = models.PositiveBigIntegerField(default=0)

    # Trophies of Mental Stats
    INT_trophies = models.PositiveBigIntegerField(default=0)
    PER_trophies = models.PositiveBigIntegerField(default=0)
    WIL_trophies = models.PositiveBigIntegerField(default=0)
    CHA_trophies = models.PositiveBigIntegerField(default=0)

    #Trophies of Physical Stats
    STR_trophies = models.PositiveBigIntegerField(default=0)
    AGI_trophies = models.PositiveBigIntegerField(default=0)
    VIT_trophies = models.PositiveBigIntegerField(default=0)
    END_trophies = models.PositiveBigIntegerField(default=0)



    def __str__(self):
        return self.user.username
    
class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50, default='Easy')
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class StatQuest(models.Model):
    STAT_CHOICES = [
        ('STR', 'Strength'), ('PER', 'Perception'), ('WIL', 'Willpower'),
        ('CHA', 'Charisma'), ('INT', 'Intelligence'), ('AGI', 'Agility'),
        ('VIT', 'Vitality'), ('END', 'Endurance')
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=STAT_CHOICES)
    difficulty = models.CharField(max_length=20, default='Easy')
    xp_reward = models.IntegerField()
    trophy_reward = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.category})"

class StatTask(models.Model):
    quest = models.ForeignKey(StatQuest, on_delete=models.CASCADE)
    task = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.task

class UserQuestProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(StatQuest, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'quest')
    
    def __str__(self):
        return f"{self.user.username} - {self.quest.name}"

class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task
