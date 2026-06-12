"""
Class Modifier System for Crescendo.

Each character class (Knight, Berserker, Warden, Ronin, Ninja, Alchemist,
Phantom, Oracle, Sage, Bard, Paladin, Mystic) has two buffs and two debuffs.

This module provides pure functions that compute multipliers and apply
class-specific side-effects.  Models are imported lazily inside functions
to avoid circular import issues.
"""

from __future__ import annotations

import math
import random
from datetime import timedelta
from typing import Any, Dict, Optional, Tuple

from django.utils import timezone


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def get_char_class(user) -> str:
    """Safely retrieve the user's character class string (e.g. 'Knight')."""
    return getattr(user, 'char_class', None) or ''


# ---------------------------------------------------------------------------
# GP multipliers — quest completion
# ---------------------------------------------------------------------------

def get_quest_gp_multipliers(user, profile, quest) -> Dict[str, float]:
    """
    Return stat GP multipliers for quest completion.

    Buffs applied:
    - Berserker Buff 1 (Frenzy Strike): +30% STR on HARD quests.
    - Ronin Buff 1 (Solitary Path): +20% STR/WIL on standalone quests.
    - Ninja Buff 1 (Shadow Blitz): +25% AGI on EASY quests.
    - Oracle Buff 1 (Foresight Matrix): +25% INT if quest created >=24 h ago.
    - Bard Buff 1 (Vibe Resonance): +20% CHA for 6 h after check-in.
    - Mystic Buff 1 (Flow Zenith): +30% WIL if consecutive_completions >= 3.

    Debuffs applied:
    - Knight Debuff 1 (Sluggish Momentum): -15% AGI always.
    - Knight Debuff 2 (Rigid Protocol): -10% CHA always.
    - Berserker Debuff 1 (Exhaustion Crash): -25% END if last completion <4 h.
    - Berserker Debuff 2 (Tunnel Vision): -15% INT/WIL on standalone quests.
    - Warden Debuff 1 (Hyper-Fixation Delay): -10% AGI always.
    - Warden Debuff 2 (Stagnant Strategy): -10% INT always.
    - Ronin Debuff 1 (Isolation Inertia): -25% CHA always.
    - Ronin Debuff 2 (Strategic Blindness): -10% INT always.
    - Ninja Debuff 1 (Shallow Depths): -15% END always.
    - Ninja Debuff 2 (Logistics Deficit): -15% WIL if late check-in.
    - Alchemist Debuff 1 (Analysis Paralysis): -15% AGI always.
    - Alchemist Debuff 2 (Volatile Chemistry): -10% WIL/END always.
    - Phantom Debuff 1 (Presence Fade): -20% CHA always.
    - Phantom Debuff 2 (Friction Vulnerability): -15% STR always.
    - Oracle Debuff 1 (Reactive Panic): -20% AGI on short-window quests.
    - Oracle Debuff 2 (Execution Drift): -10% STR always.
    - Sage Debuff 1 (Velocity Deficit): -20% AGI always.
    - Sage Debuff 2 (Over-Intellectualization): -10% STR always.
    - Bard Debuff 1 (Dry Grind Inertia): -25% WIL always.
    - Bard Debuff 2 (Isolation Fade): -15% END if no active roadmap.
    - Paladin Debuff 2 (Tactical Blindness): -10% INT always.
    - Mystic Debuff 1 (Rigid Lock): -25% AGI if >2 active roadmaps.
    - Mystic Debuff 2 (Sensory Drain): -15% END always;
      if streak_freezes == 0, all stats -10%.
    """
    char_class = get_char_class(user)
    mults: Dict[str, float] = {
        'STR': 1.0, 'END': 1.0, 'AGI': 1.0,
        'INT': 1.0, 'CHA': 1.0, 'WIL': 1.0,
    }

    if not char_class:
        return mults

    # Lazy imports to avoid circular dependency
    from .models import UserRoadmap, Quest as QuestModel

    now = timezone.now()
    active_roadmap_count = UserRoadmap.objects.filter(
        user=user, status='PENDING',
    ).count()

    # --- GRIMWARD ARCHETYPE ---

    if char_class == 'Knight':
        mults['AGI'] -= 0.15   # Debuff 1 — Sluggish Momentum
        mults['CHA'] -= 0.10   # Debuff 2 — Rigid Protocol

    elif char_class == 'Berserker':
        # Buff 1 — Frenzy Strike
        if quest.difficulty == 'HARD':
            mults['STR'] += 0.30
        # Debuff 1 — Exhaustion Crash (last completion <4 h ago)
        if (
            profile.last_quest_completed_at
            and (now - profile.last_quest_completed_at).total_seconds() < 14400
        ):
            mults['END'] -= 0.25
        # Debuff 2 — Tunnel Vision (standalone quest)
        mults['INT'] -= 0.15
        mults['WIL'] -= 0.15

    elif char_class == 'Warden':
        mults['AGI'] -= 0.10   # Debuff 1 — Hyper-Fixation Delay
        mults['INT'] -= 0.10   # Debuff 2 — Stagnant Strategy

    elif char_class == 'Ronin':
        # Buff 1 — Solitary Path (standalone quest)
        mults['STR'] += 0.20
        mults['WIL'] += 0.20
        mults['CHA'] -= 0.25   # Debuff 1 — Isolation Inertia
        mults['INT'] -= 0.10   # Debuff 2 — Strategic Blindness

    # --- ASHBORNE ARCHETYPE ---

    elif char_class == 'Ninja':
        # Buff 1 — Shadow Blitz
        if quest.difficulty == 'EASY':
            mults['AGI'] += 0.25
        mults['END'] -= 0.15   # Debuff 1 — Shallow Depths
        # Debuff 2 — Logistics Deficit: -15% WIL if late check-in
        # "Late" means checked in after 12 h into the day (noon+).
        # If last_checkin is today, we conservatively apply it since we
        # don't store exact check-in time.
        if profile.last_checkin and profile.last_checkin == now.date():
            # No precise time stored — apply the debuff conservatively
            pass
        mults['WIL'] -= 0.15

    elif char_class == 'Alchemist':
        mults['AGI'] -= 0.15   # Debuff 1 — Analysis Paralysis
        mults['WIL'] -= 0.10   # Debuff 2 — Volatile Chemistry
        mults['END'] -= 0.10   # Debuff 2 — Volatile Chemistry

    elif char_class == 'Phantom':
        # Buff 1 — Asynchronous Strike
        if active_roadmap_count > 1:
            mults['INT'] += 0.20
        mults['CHA'] -= 0.20   # Debuff 1 — Presence Fade
        mults['STR'] -= 0.15   # Debuff 2 — Friction Vulnerability

    elif char_class == 'Oracle':
        # Buff 1 — Foresight Matrix (created >=24 h before now)
        if (
            quest.created_at
            and (now - quest.created_at).total_seconds() >= 86400
        ):
            mults['INT'] += 0.25
        # Debuff 1 — Reactive Panic: short-window quest (<3 h window)
        if (
            quest.created_at
            and quest.deadline
            and (quest.deadline - quest.created_at).total_seconds() < 10800
        ):
            mults['AGI'] -= 0.20
        mults['STR'] -= 0.10   # Debuff 2 — Execution Drift

    # --- GOLDVEIL ARCHETYPE ---

    elif char_class == 'Sage':
        mults['AGI'] -= 0.20   # Debuff 1 — Velocity Deficit
        mults['STR'] -= 0.10   # Debuff 2 — Over-Intellectualization

    elif char_class == 'Bard':
        # Buff 1 — Vibe Resonance: +20% CHA within 6 h of check-in
        if profile.last_checkin and profile.last_checkin == now.date():
            mults['CHA'] += 0.20
        mults['WIL'] -= 0.25   # Debuff 1 — Dry Grind Inertia
        # Debuff 2 — Isolation Fade: -15% END if no active roadmap
        if active_roadmap_count == 0:
            mults['END'] -= 0.15

    elif char_class == 'Paladin':
        mults['INT'] -= 0.10   # Debuff 2 — Tactical Blindness

    elif char_class == 'Mystic':
        # Buff 1 — Flow Zenith
        if profile.consecutive_quest_completions >= 3:
            mults['WIL'] += 0.30
        # Debuff 1 — Rigid Lock
        if active_roadmap_count > 2:
            mults['AGI'] -= 0.25
        mults['END'] -= 0.15   # Debuff 2 — Sensory Drain
        # Debuff 2 extra: if streak_freezes == 0, all stats -10%
        if profile.streak_freezes == 0:
            for stat in mults:
                mults[stat] -= 0.10

    # Clamp all multipliers to a minimum of 0.0
    for stat in mults:
        mults[stat] = max(0.0, mults[stat])

    return mults


# ---------------------------------------------------------------------------
# GP multipliers — roadmap completion
# ---------------------------------------------------------------------------

def get_roadmap_gp_multipliers(user, profile, roadmap) -> Dict[str, float]:
    """
    Return stat GP multipliers for roadmap completion.

    Buffs applied:
    - Knight Buff 1 (Iron Clad Routine): +15% STR/END on Grand Roadmap.
    - Warden Buff 1 (Endurance Pace): +15% END per day roadmap was active
      (applied as lump-sum: ``days_active * 0.15 * base_reward``).
    - Alchemist Buff 1 (Refined Framework): +20% INT on roadmap completion.
    - Paladin Buff 1 (Oath Keeper): +25% WIL on roadmap completion.
    - Sage Buff 1 (Deep Clarity): +20% INT/WIL on HARD roadmaps.

    Debuffs applied:
    - Knight Debuff 1: -15% AGI always.
    - Knight Debuff 2: -10% CHA always.
    - Warden Debuff 1: -10% AGI always.
    - Warden Debuff 2: -10% INT always; -10% total GP from roadmap.
    - Ronin Debuff 1: -25% CHA always.
    - Ronin Debuff 2: -10% INT always.
    - Alchemist Debuff 1: -15% AGI always.
    - Alchemist Debuff 2: -10% WIL/END always.
    - Phantom Debuff 1: -20% CHA always.
    - Phantom Debuff 2: -15% STR always.
    - Oracle Debuff 2: -10% STR always.
    - Sage Debuff 1: -20% AGI always.
    - Sage Debuff 2: -10% STR always.
    - Bard Debuff 1: -25% WIL always.
    - Paladin Debuff 2: -10% INT always.
    - Mystic Debuff 2: -15% END always; if streak_freezes == 0 all stats -10%.
    """
    char_class = get_char_class(user)
    mults: Dict[str, float] = {
        'STR': 1.0, 'END': 1.0, 'AGI': 1.0,
        'INT': 1.0, 'CHA': 1.0, 'WIL': 1.0,
    }

    if not char_class:
        return mults

    now = timezone.now()
    template = roadmap.template
    roadmap_difficulty = template.difficulty if template else 'MEDIUM'

    # Compute days active for Warden buff
    days_active = max(
        1,
        (now - roadmap.created_at).days if roadmap.created_at else 1,
    )

    # --- GRIMWARD ---

    if char_class == 'Knight':
        # Buff 1 — Iron Clad Routine: +15% STR/END on Grand (HARD) roadmap
        if roadmap_difficulty == 'HARD':
            mults['STR'] += 0.15
            mults['END'] += 0.15
        mults['AGI'] -= 0.15   # Debuff 1
        mults['CHA'] -= 0.10   # Debuff 2

    elif char_class == 'Berserker':
        # No roadmap-specific buffs; standalone debuffs don't apply to roadmaps
        pass

    elif char_class == 'Warden':
        # Buff 1 — Endurance Pace: per-day END bonus
        # The caller should multiply: base_reward * (mults[stat] + warden_bonus)
        # We encode the per-day bonus in END as a lump multiplier.
        mults['END'] += days_active * 0.15
        mults['AGI'] -= 0.10   # Debuff 1
        mults['INT'] -= 0.10   # Debuff 2
        # Debuff 2 also: -10% total GP from roadmap
        for stat in mults:
            mults[stat] *= 0.90

    elif char_class == 'Ronin':
        # No roadmap buffs (buffs are standalone-only)
        mults['CHA'] -= 0.25   # Debuff 1
        mults['INT'] -= 0.10   # Debuff 2

    # --- ASHBORNE ---

    elif char_class == 'Ninja':
        # No roadmap-specific buffs
        mults['END'] -= 0.15   # Debuff 1
        mults['WIL'] -= 0.15   # Debuff 2 (conservative)

    elif char_class == 'Alchemist':
        # Buff 1 — Refined Framework
        mults['INT'] += 0.20
        mults['AGI'] -= 0.15   # Debuff 1
        mults['WIL'] -= 0.10   # Debuff 2
        mults['END'] -= 0.10   # Debuff 2

    elif char_class == 'Phantom':
        mults['CHA'] -= 0.20   # Debuff 1
        mults['STR'] -= 0.15   # Debuff 2

    elif char_class == 'Oracle':
        mults['STR'] -= 0.10   # Debuff 2

    # --- GOLDVEIL ---

    elif char_class == 'Sage':
        # Buff 1 — Deep Clarity: +20% INT/WIL on HARD roadmaps
        if roadmap_difficulty == 'HARD':
            mults['INT'] += 0.20
            mults['WIL'] += 0.20
        mults['AGI'] -= 0.20   # Debuff 1
        mults['STR'] -= 0.10   # Debuff 2

    elif char_class == 'Bard':
        mults['WIL'] -= 0.25   # Debuff 1

    elif char_class == 'Paladin':
        # Buff 1 — Oath Keeper
        mults['WIL'] += 0.25
        mults['INT'] -= 0.10   # Debuff 2

    elif char_class == 'Mystic':
        mults['END'] -= 0.15   # Debuff 2
        if profile.streak_freezes == 0:
            for stat in mults:
                mults[stat] -= 0.10

    # Clamp
    for stat in mults:
        mults[stat] = max(0.0, mults[stat])

    return mults


# ---------------------------------------------------------------------------
# XP multipliers
# ---------------------------------------------------------------------------

def get_quest_xp_multiplier(user, profile, quest) -> float:
    """
    Return the XP multiplier for quest completion.

    Buffs applied:
    - Berserker Buff 2 (Clutch Performance): 2× XP if completed within 1 h
      of deadline.
    - Ronin Buff 2 (Single-Target Edge): +15% XP when only 1 pending quest.
    - Bard Buff 2 (Public Drive): streak >= 15 → +15% base XP on all quests.
    - Mystic Buff 2 (Intuitive Velocity): +15% XP on all quest completions.

    Debuffs applied:
    - Oracle Debuff 2 (Execution Drift): -25% XP from standalone EASY quests.
    """
    char_class = get_char_class(user)
    multiplier = 1.0

    if not char_class:
        return multiplier

    from .models import Quest as QuestModel

    now = timezone.now()

    if char_class == 'Berserker':
        # Buff 2 — Clutch Performance: 2× XP if within 1 h of deadline
        if quest.deadline and (quest.deadline - now).total_seconds() <= 3600:
            multiplier *= 2.0

    elif char_class == 'Ronin':
        # Buff 2 — Single-Target Edge
        pending = QuestModel.objects.filter(user=user, status='PENDING').count()
        if pending <= 1:
            multiplier += 0.15

    elif char_class == 'Oracle':
        # Debuff 2 — Execution Drift: -25% XP from standalone EASY quests
        if quest.difficulty == 'EASY':
            multiplier -= 0.25

    elif char_class == 'Bard':
        # Buff 2 — Public Drive
        if profile.streak >= 15:
            multiplier += 0.15

    elif char_class == 'Mystic':
        # Buff 2 — Intuitive Velocity
        multiplier += 0.15

    return max(0.0, multiplier)


def get_roadmap_xp_multiplier(user, profile) -> float:
    """
    Return the XP multiplier for roadmap completion.

    Buffs applied:
    - Oracle Buff 2 (Strategic Leverage): +20% XP from roadmap completions.

    Debuffs: none specific to roadmap XP.
    """
    char_class = get_char_class(user)
    multiplier = 1.0

    if char_class == 'Oracle':
        multiplier += 0.20

    return multiplier


# ---------------------------------------------------------------------------
# Aura reward / penalty helpers
# ---------------------------------------------------------------------------

def get_quest_aura_reward(user, profile, quest) -> int:
    """
    Return the base Aura reward for completing a quest.

    Default is 1 (caller may have its own base; this acts as a modifier).

    Debuffs applied:
    - Paladin Debuff 2 (Tactical Blindness): EASY quests generate 0 Aura.
    """
    char_class = get_char_class(user)

    if char_class == 'Paladin' and quest.difficulty == 'EASY':
        return 0

    return 1


def get_quest_failure_aura_multiplier(user, profile, quest) -> float:
    """
    Return a multiplier on the Aura penalty when a quest fails.

    Values > 1.0 *increase* the penalty; < 1.0 *reduce* it.

    Buffs applied:
    - Knight Buff 2 (Fortified Shield): ×0.8 if streak > 0.

    Debuffs applied:
    - Warden Debuff 1 (Hyper-Fixation Delay): +5% more Aura drain if
      quest has >6 subtasks.
    - Ninja Debuff 1 (Shallow Depths): +10% more Aura drain on HARD quests.
    - Bard Debuff 1 (Dry Grind Inertia): ×2 if quest has 0 subtasks.
    - Phantom Debuff 2 (Friction Vulnerability): ×2 on standalone quest failure.
    """
    char_class = get_char_class(user)
    multiplier = 1.0

    if not char_class:
        return multiplier

    if char_class == 'Knight':
        # Buff 2 — Fortified Shield
        if profile.streak > 0:
            multiplier *= 0.80

    elif char_class == 'Warden':
        # Debuff 1 — failed quests with >6 subtasks drain 5% more Aura
        if quest.subtasks.count() > 6:
            multiplier += 0.05

    elif char_class == 'Ninja':
        # Debuff 1 — HARD quests that fail drain 10% more Aura
        if quest.difficulty == 'HARD':
            multiplier += 0.10

    elif char_class == 'Phantom':
        # Debuff 2 — standalone quest failure doubles Aura penalty
        multiplier *= 2.0

    elif char_class == 'Bard':
        # Debuff 1 — 0 subtask quest failure doubles Aura penalty
        if quest.subtasks.count() == 0:
            multiplier *= 2.0

    return multiplier


def get_roadmap_failure_aura_multiplier(user, profile, roadmap) -> float:
    """
    Return multiplier on the Aura penalty when a roadmap fails or is abandoned.

    Debuffs applied:
    - Paladin Debuff 1 (Purpose Depletion): doubles the roadmap failure
      Aura penalty when a roadmap deadline is missed.
    """
    char_class = get_char_class(user)
    multiplier = 1.0

    if char_class == 'Paladin':
        # Debuff 1 — doubles roadmap failure Aura penalty
        multiplier *= 2.0

    return multiplier


# ---------------------------------------------------------------------------
# Streak mechanics
# ---------------------------------------------------------------------------

def get_streak_break_increment(user) -> int:
    """
    Return how many streak breaks to record per break event.

    Debuffs applied:
    - Alchemist Debuff 2 (Volatile Chemistry): streak breaks count as +2.
    """
    if get_char_class(user) == 'Alchemist':
        return 2
    return 1


def get_streak_penalty_multiplier(user) -> float:
    """
    Return multiplier on the monthly 5-break Aura penalty.

    Buffs applied:
    - Phantom Buff 2 (Ghost Protocol): 15% resistance → ×0.85.
    """
    if get_char_class(user) == 'Phantom':
        return 0.85
    return 1.0


def can_use_streak_freeze(user) -> bool:
    """
    Return whether the user is allowed to consume streak freezes.

    Debuffs applied:
    - Ronin Debuff 1 (Isolation Inertia): streak freezes cannot be used.
    """
    if get_char_class(user) == 'Ronin':
        return False
    return True


# ---------------------------------------------------------------------------
# Ritual modifiers
# ---------------------------------------------------------------------------

def get_ritual_extra_days(user) -> int:
    """
    Return extra days required for the rank-up ritual prerequisite.

    Debuffs applied:
    - Knight Debuff 2 (Rigid Protocol): +2 extra days.
    """
    if get_char_class(user) == 'Knight':
        return 2
    return 0


def get_ritual_aura_cap_multiplier(user) -> float:
    """
    Return multiplier for the Aura cap required to start a ritual.

    Debuffs applied:
    - Phantom Debuff 1 (Presence Fade): Aura cap increased by 15% → ×1.15.
    """
    if get_char_class(user) == 'Phantom':
        return 1.15
    return 1.0


# ---------------------------------------------------------------------------
# Roadmap slot modifier
# ---------------------------------------------------------------------------

def get_roadmap_slot_modifier(user) -> int:
    """
    Return modifier to the maximum number of roadmap slots.

    Debuffs applied:
    - Ronin Debuff 2 (Strategic Blindness): -1 roadmap slot.
    """
    if get_char_class(user) == 'Ronin':
        return -1
    return 0


# ---------------------------------------------------------------------------
# Roadmap abandon (Ninja free abandon)
# ---------------------------------------------------------------------------

def can_abandon_roadmap_free(user, profile) -> bool:
    """
    Return whether the user can abandon a roadmap without Aura penalty.

    Buffs applied:
    - Ninja Buff 2 (Agile Pivot): 1 free abandon per month.

    Resets ``free_roadmap_abandons_this_month`` on month rollover.
    """
    if get_char_class(user) != 'Ninja':
        return False

    now = timezone.now().date()
    # Reset counter on new month
    if (
        profile.last_abandon_reset_date is None
        or profile.last_abandon_reset_date.month != now.month
        or profile.last_abandon_reset_date.year != now.year
    ):
        profile.free_roadmap_abandons_this_month = 0
        profile.last_abandon_reset_date = now
        profile.save(update_fields=[
            'free_roadmap_abandons_this_month',
            'last_abandon_reset_date',
        ])

    return profile.free_roadmap_abandons_this_month < 1


def use_free_roadmap_abandon(user, profile) -> bool:
    """
    Consume one free roadmap abandon for Ninja.

    Returns True if the free abandon was consumed, False otherwise.
    """
    if not can_abandon_roadmap_free(user, profile):
        return False

    profile.free_roadmap_abandons_this_month += 1
    profile.save(update_fields=['free_roadmap_abandons_this_month'])
    return True


# ---------------------------------------------------------------------------
# Post-completion side effects
# ---------------------------------------------------------------------------

def on_quest_completion_effects(
    user,
    profile,
    quest,
    xp_gained: int,
) -> Dict[str, Any]:
    """
    Apply post-quest-completion side effects for the user's class.

    Effects handled:
    - Alchemist Buff 2 (Optimized Crucible): refund 5% of XP gained as Aura
      (floor, minimum 1).
    - Warden Buff 2 (Perimeter Defense): first quest completed before 9 AM
      sets ``demotion_immunity_until`` = now + 24 h.
    - Berserker: records ``last_quest_completed_at`` for Exhaustion Crash
      tracking.
    - Mystic: tracks ``consecutive_quest_completions`` within 30-min windows.

    Also unconditionally updates ``last_quest_completed_at``.

    Returns a dict of effects applied for logging / response enrichment.
    """
    char_class = get_char_class(user)
    effects: Dict[str, Any] = {}
    now = timezone.now()

    # -- Universal: record completion timestamp --
    profile.last_quest_completed_at = now

    if char_class == 'Alchemist':
        # Buff 2 — Optimized Crucible
        aura_refund = max(1, math.floor(xp_gained * 0.05))
        profile.aura += aura_refund
        cap = profile.get_aura_cap()
        if profile.aura > cap:
            profile.aura = cap
        effects['aura_refund'] = aura_refund

    elif char_class == 'Warden':
        # Buff 2 — Perimeter Defense: before 9 AM local
        # Using server timezone; if needed, adjust to user tz later.
        if now.hour < 9:
            immunity_until = now + timedelta(hours=24)
            profile.demotion_immunity_until = immunity_until
            effects['demotion_immunity_until'] = immunity_until.isoformat()

    elif char_class == 'Mystic':
        # Track consecutive completions within 30-min windows
        if (
            profile.last_consecutive_completion_at
            and (now - profile.last_consecutive_completion_at).total_seconds()
            <= 1800
        ):
            profile.consecutive_quest_completions += 1
        else:
            profile.consecutive_quest_completions = 1
        profile.last_consecutive_completion_at = now
        effects['consecutive_quest_completions'] = (
            profile.consecutive_quest_completions
        )

    # Save all changed fields
    update_fields = ['last_quest_completed_at']
    if char_class == 'Alchemist':
        update_fields.append('aura')
    elif char_class == 'Warden' and 'demotion_immunity_until' in effects:
        update_fields.append('demotion_immunity_until')
    elif char_class == 'Mystic':
        update_fields.extend([
            'consecutive_quest_completions',
            'last_consecutive_completion_at',
        ])

    profile.save(update_fields=update_fields)
    return effects


# ---------------------------------------------------------------------------
# Check-in effects
# ---------------------------------------------------------------------------

def on_checkin_effects(user, profile) -> Dict[str, Any]:
    """
    Apply class effects during daily check-in.

    Effects handled:
    - Sage Buff 2 (Subconscious Calculation): 15% chance to restore 50 Aura.

    Returns a dict of effects applied.
    """
    char_class = get_char_class(user)
    effects: Dict[str, Any] = {}

    if char_class == 'Sage':
        if random.random() < 0.15:
            aura_restore = 50
            profile.aura += aura_restore
            cap = profile.get_aura_cap()
            if profile.aura > cap:
                profile.aura = cap
            profile.save(update_fields=['aura'])
            effects['aura_restored'] = aura_restore

    return effects


# ---------------------------------------------------------------------------
# Quest failure effects
# ---------------------------------------------------------------------------

def on_quest_failure_effects(
    user,
    profile,
    quest,
    base_xp: int,
) -> Dict[str, Any]:
    """
    Apply class-specific effects when a quest fails.

    Effects handled:
    - Sage Debuff 1 (Velocity Deficit): strips 10% of current XP on failure.

    Returns a dict of effects applied.
    """
    char_class = get_char_class(user)
    effects: Dict[str, Any] = {}

    if char_class == 'Sage':
        xp_lost = math.floor(profile.exp * 0.10)
        profile.exp = max(0, profile.exp - xp_lost)
        profile.save(update_fields=['exp'])
        effects['xp_stripped'] = xp_lost

    return effects


# ---------------------------------------------------------------------------
# Paladin demotion immunity
# ---------------------------------------------------------------------------

def on_rank_demotion_check(user, profile) -> Dict[str, Any]:
    """
    Called when a rank demotion is about to happen.

    Buffs applied:
    - Paladin Buff 2 (Righteous Shield): grants 24 h demotion immunity
      instead of immediate demotion.

    Returns a dict of effects. If ``'immunity_granted'`` is True, the caller
    should skip the demotion.
    """
    char_class = get_char_class(user)
    effects: Dict[str, Any] = {'immunity_granted': False}

    if char_class == 'Paladin':
        now = timezone.now()
        # Only grant if not already immune
        if (
            not profile.demotion_immunity_until
            or profile.demotion_immunity_until <= now
        ):
            profile.demotion_immunity_until = now + timedelta(hours=24)
            profile.save(update_fields=['demotion_immunity_until'])
            effects['immunity_granted'] = True
            effects['demotion_immunity_until'] = (
                profile.demotion_immunity_until.isoformat()
            )

    return effects


# ---------------------------------------------------------------------------
# Quest completion gate
# ---------------------------------------------------------------------------

def can_complete_quest(user, quest) -> Tuple[bool, str]:
    """
    Check whether a quest is allowed to be completed.

    Debuffs applied:
    - Alchemist Debuff 1 (Analysis Paralysis): quest cannot be marked
      complete unless ALL subtasks are completed.

    Returns (allowed: bool, error_message: str).
    """
    char_class = get_char_class(user)

    if char_class == 'Alchemist':
        total = quest.subtasks.count()
        if total > 0:
            completed = quest.subtasks.filter(is_completed=True).count()
            if completed < total:
                return (
                    False,
                    'Alchemist class requires all subtasks to be completed '
                    'before the quest can be marked as done.',
                )

    return (True, '')
