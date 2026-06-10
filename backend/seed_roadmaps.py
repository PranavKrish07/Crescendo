import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from dashboard.models import RoadmapTemplate

# Clear existing templates
RoadmapTemplate.objects.all().delete()

ROADMAPS = [
    # STR (Strength)
    {
        'title': 'The Iron Foundations',
        'description': 'A beginner roadmap to build fundamental strength.',
        'stat': 'STR',
        'difficulty': 'EASY',
        'tasks': [f'Strength Task {i}' for i in range(1, 11)] # 10 tasks
    },
    {
        'title': 'The Titan\'s Path',
        'description': 'An advanced routine focusing on heavy lifting and explosive power.',
        'stat': 'STR',
        'difficulty': 'HARD',
        'tasks': [f'Advanced Lift {i}' for i in range(1, 56)] # 55 tasks
    },

    # END (Endurance)
    {
        'title': 'Marathon Primer',
        'description': 'Build your cardiovascular base.',
        'stat': 'END',
        'difficulty': 'MEDIUM',
        'tasks': [f'Endurance Run {i}' for i in range(1, 26)] # 25 tasks
    },
    {
        'title': 'The Iron Lungs Challenge',
        'description': 'Extreme endurance conditioning for elite stamina.',
        'stat': 'END',
        'difficulty': 'HARD',
        'tasks': [f'Endurance Trial {i}' for i in range(1, 61)] # 60 tasks
    },

    # AGI (Agility)
    {
        'title': 'Nimble Footwork',
        'description': 'Basic agility drills to improve coordination and speed.',
        'stat': 'AGI',
        'difficulty': 'EASY',
        'tasks': [f'Agility Drill {i}' for i in range(1, 13)] # 12 tasks
    },
    {
        'title': 'The Shadow Dancer',
        'description': 'Complex movements and reflexes training.',
        'stat': 'AGI',
        'difficulty': 'MEDIUM',
        'tasks': [f'Reflex Drill {i}' for i in range(1, 31)] # 30 tasks
    },

    # INT (Intelligence)
    {
        'title': 'The Scholar\'s Awakening',
        'description': 'Introductory reading and cognitive exercises.',
        'stat': 'INT',
        'difficulty': 'EASY',
        'tasks': [f'Study Session {i}' for i in range(1, 15)] # 14 tasks
    },
    {
        'title': 'The Archmage Archives',
        'description': 'Deep research, logic puzzles, and complex problem solving.',
        'stat': 'INT',
        'difficulty': 'HARD',
        'tasks': [f'Logic Puzzle {i}' for i in range(1, 51)] # 50 tasks
    },

    # CHA (Charisma)
    {
        'title': 'The Social Butterfly',
        'description': 'Exercises to improve public speaking and small talk.',
        'stat': 'CHA',
        'difficulty': 'MEDIUM',
        'tasks': [f'Social Interaction {i}' for i in range(1, 21)] # 20 tasks
    },
    {
        'title': 'The Diplomat\'s Journey',
        'description': 'Master negotiation, persuasion, and leadership.',
        'stat': 'CHA',
        'difficulty': 'HARD',
        'tasks': [f'Leadership Challenge {i}' for i in range(1, 55)] # 54 tasks
    },

    # WIL (Willpower)
    {
        'title': 'The Unbroken Mind',
        'description': 'Daily meditation and habit-forming exercises.',
        'stat': 'WIL',
        'difficulty': 'EASY',
        'tasks': [f'Meditation Session {i}' for i in range(1, 11)] # 10 tasks
    },
    {
        'title': 'The Stoic Fortress',
        'description': 'Rigorous mental resilience and discipline conditioning.',
        'stat': 'WIL',
        'difficulty': 'MEDIUM',
        'tasks': [f'Discipline Challenge {i}' for i in range(1, 40)] # 39 tasks
    },
]

for rm in ROADMAPS:
    RoadmapTemplate.objects.create(
        title=rm['title'],
        description=rm['description'],
        stat=rm['stat'],
        difficulty=rm['difficulty'],
        tasks=rm['tasks']
    )

print(f"Successfully seeded {len(ROADMAPS)} roadmap templates.")
