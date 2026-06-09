from django.utils import timezone
from .models import Quest, UserProfile

def process_quest_completion(quest):
    """Handles XP, Aura, and fractional stat rewards when a quest is completed."""
    if quest.status == 'COMPLETED':
        return  # already completed
    
    profile = quest.user.profile

    # Base Aura Reward
    profile.aura += 1

    # Fractional stat rewards
    if quest.stat:
        stat_field = f"{quest.stat.lower()}_points"
        current_val = getattr(profile, stat_field, 0)
        setattr(profile, stat_field, current_val + 0.25)
    
    # XP Reward based on difficulty
    xp_rewards = {
        'EASY': 50,
        'MEDIUM': 100,
        'HARD': 200,
    }
    xp_gained = xp_rewards.get(quest.difficulty, 50)
    profile.add_exp(xp_gained)

    quest.status = 'COMPLETED'
    quest.save()


def evaluate_daily_quests(user):
    """
    Lazy evaluation: find all pending daily quests whose deadline has passed.
    Mark them as FAILED and deduct 1 Aura point per failure.
    """
    profile = user.profile
    now = timezone.now()
    expired_quests = Quest.objects.filter(
        user=user, 
        is_daily=True, 
        status='PENDING', 
        deadline__lt=now
    )

    if expired_quests.exists():
        failures = expired_quests.count()
        profile.aura -= failures
        profile.save()
        expired_quests.update(status='FAILED')
