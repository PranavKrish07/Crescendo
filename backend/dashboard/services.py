from django.utils import timezone
from .models import Quest, UserProfile

def process_quest_completion(quest):
    """Handles XP, Aura, and fractional stat rewards when a quest is completed."""
    if quest.status == 'COMPLETED':
        return  # already completed
    
    profile = quest.user.profile

    # Base Aura Reward
    profile.add_aura(1)

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


def evaluate_expired_quests(user):
    """
    Lazy evaluation: find all pending quests whose deadline has passed.
    Mark them as FAILED and deduct Aura points.
    - Normal quests: -2 aura
    - Daily quests: -5 aura
    """
    profile = user.profile
    now = timezone.now()
    expired_quests = Quest.objects.filter(
        user=user, 
        status='PENDING', 
        deadline__date__lt=now.date()
    )

    if expired_quests.exists():
        aura_loss = 0
        for quest in expired_quests:
            if quest.is_daily:
                aura_loss += 5
            else:
                aura_loss += 2
                
        profile.aura -= aura_loss
        profile.save()
        profile.update_rank()
        expired_quests.update(status='FAILED')

def get_roadmap_aura_reward(rank, difficulty):
    """Returns the Aura reward/penalty for a roadmap based on rank and difficulty."""
    rewards = {
        'EASY': {'E': 50, 'D': 65, 'C': 80, 'B': 100, 'A': 130, 'S': 150},
        'MEDIUM': {'E': 50, 'D': 65, 'C': 80, 'B': 100, 'A': 130, 'S': 150},
        'HARD': {'E': 60, 'D': 75, 'C': 90, 'B': 110, 'A': 140, 'S': 160},
    }
    diff_map = rewards.get(difficulty, rewards['MEDIUM'])
    return diff_map.get(rank, diff_map['E'])

def evaluate_expired_roadmaps(user):
    """
    Finds all pending roadmaps whose deadline has passed.
    Marks them as FAILED and deducts the corresponding Aura points.
    """
    from .models import UserRoadmap # Import here to avoid circular imports
    profile = user.profile
    now = timezone.now()
    
    expired_roadmaps = UserRoadmap.objects.filter(
        user=user,
        status='PENDING',
        deadline__lt=now
    )
    
    if expired_roadmaps.exists():
        for r in expired_roadmaps:
            penalty = get_roadmap_aura_reward(profile.rank, r.template.difficulty)
            # Use profile.aura directly instead of add_aura to allow dropping below thresholds easily
            # But wait, add_aura handles clamping. A penalty just subtracts. 
            # I will just subtract.
            profile.aura -= penalty
            
        profile.save()
        profile.update_rank()
        expired_roadmaps.update(status='FAILED')
