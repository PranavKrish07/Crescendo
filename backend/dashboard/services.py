from django.utils import timezone
from .models import Quest, UserProfile
from . import class_modifiers


def process_quest_completion(quest):
    """Handles XP, Aura, and fractional stat rewards when a quest is completed.
    
    Integrates the class modifier system for:
    - GP multipliers per stat (class_modifiers.get_quest_gp_multipliers)
    - XP multipliers (class_modifiers.get_quest_xp_multiplier)
    - Aura reward modifiers (class_modifiers.get_quest_aura_reward)
    - Post-completion side effects (class_modifiers.on_quest_completion_effects)
    - Quest completion gating (class_modifiers.can_complete_quest)
    """
    if quest.status == 'COMPLETED':
        return  # already completed
    
    user = quest.user
    profile = quest.user.profile

    # --- Class gate: Alchemist cannot complete unless all subtasks done ---
    allowed, error_msg = class_modifiers.can_complete_quest(user, quest)
    if not allowed:
        return  # Silently block; the view layer should check this first

    # --- Base Aura Reward (modified by class) ---
    aura_reward = class_modifiers.get_quest_aura_reward(user, profile, quest)
    if aura_reward > 0:
        profile.add_aura(aura_reward)

    # --- Fractional stat rewards with class GP multipliers ---
    if quest.stat:
        gp_multipliers = class_modifiers.get_quest_gp_multipliers(user, profile, quest)
        stat_key = quest.stat.upper()
        stat_field = f"{quest.stat.lower()}_points"
        current_val = getattr(profile, stat_field, 0)
        base_gp = 0.25
        multiplied_gp = base_gp * gp_multipliers.get(stat_key, 1.0)
        setattr(profile, stat_field, current_val + multiplied_gp)
    
    # --- XP Reward with class XP multiplier ---
    xp_rewards = {
        'EASY': 50,
        'MEDIUM': 100,
        'HARD': 200,
    }
    base_xp = xp_rewards.get(quest.difficulty, 50)
    xp_multiplier = class_modifiers.get_quest_xp_multiplier(user, profile, quest)
    xp_gained = int(base_xp * xp_multiplier)
    profile.add_exp(xp_gained)

    # --- Post-completion class effects (Alchemist Aura refund, Warden immunity, Mystic combo) ---
    class_modifiers.on_quest_completion_effects(user, profile, quest, xp_gained)

    quest.status = 'COMPLETED'
    quest.save()


def evaluate_expired_quests(user):
    """
    Lazy evaluation: find all pending quests whose deadline has passed.
    Mark them as FAILED and deduct Aura points.
    - Normal quests: -2 aura (modified by class failure multiplier)
    - Daily quests: -5 aura (modified by class failure multiplier)
    
    Integrates class modifiers:
    - Aura penalty multiplier (Knight shield, Phantom double, Bard zero-subtask, etc.)
    - Quest failure effects (Sage XP strip)
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
            # Base penalty
            if quest.is_daily:
                base_penalty = 5
            else:
                base_penalty = 2

            # Apply class failure Aura multiplier
            failure_mult = class_modifiers.get_quest_failure_aura_multiplier(
                user, profile, quest
            )
            aura_loss += int(base_penalty * failure_mult)

            # Apply class failure side effects (e.g., Sage XP strip)
            class_modifiers.on_quest_failure_effects(user, profile, quest, base_penalty)
                
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
    
    Integrates class modifiers:
    - Roadmap failure Aura multiplier (Paladin doubles penalty)
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
            base_penalty = get_roadmap_aura_reward(profile.rank, r.template.difficulty)
            # Apply class failure multiplier
            failure_mult = class_modifiers.get_roadmap_failure_aura_multiplier(
                user, profile, r
            )
            penalty = int(base_penalty * failure_mult)
            profile.aura -= penalty
            
        profile.save()
        profile.update_rank()
        expired_roadmaps.update(status='FAILED')
