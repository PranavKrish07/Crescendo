SCENES = [
    {
        "id": 1,
        "label": "Scene I \u2014 The Burning Village",
        "title": "Fire and Smoke",
        "narrative": "You wake to the smell of burning thatch. A wooden beam has pinned a stranger to the ground. The fire is spreading fast, and no one else has stopped to help.",
        "question": "What do you do?",
        "choices": [
            {"text": "You lift the beam without thinking. Your arms scream, but you don\u2019t stop.", "stats": {"STR": 3, "END": 2}},
            {"text": "You scan the fire, find the safe angle, then move the beam with leverage.", "stats": {"INT": 3, "AGI": 2}},
            {"text": "You rally nearby strangers to help carry the beam together.", "stats": {"CHA": 3, "WIL": 2}},
            {"text": "Every part of you wants to run \u2014 you stay anyway.", "stats": {"WIL": 3, "END": 2}},
        ]
    },
    {
        "id": 2,
        "label": "Scene II \u2014 The Merchant\u2019s Dilemma",
        "title": "Crossroads Deal",
        "narrative": "A merchant offers you a map to a hidden treasure \u2014 but the price is a favor to be named later. His smile is too wide. The treasure could change everything.",
        "question": "How do you respond?",
        "choices": [
            {"text": "You decline. Debt to a stranger is a chain you refuse to wear.", "stats": {"WIL": 3, "INT": 2}},
            {"text": "You negotiate hard \u2014 half now, half on delivery, no open favors.", "stats": {"CHA": 3, "INT": 2}},
            {"text": "You accept. Fortune favors those who move first.", "stats": {"AGI": 3, "STR": 2}},
            {"text": "You memorize the map from a glance, then walk away.", "stats": {"INT": 3, "AGI": 2}},
        ]
    },
    {
        "id": 3,
        "label": "Scene III \u2014 The Wounded Rival",
        "title": "Blood in the Snow",
        "narrative": "Your rival lies bleeding in the snow after an ambush. They once humiliated you in front of everyone. Now they need your help to survive the night.",
        "question": "What is your move?",
        "choices": [
            {"text": "You tend their wounds in silence. Grudges are for the weak.", "stats": {"WIL": 3, "CHA": 2}},
            {"text": "You help, but make sure they know the debt they now owe.", "stats": {"CHA": 3, "STR": 2}},
            {"text": "You stabilize them quickly and scout the area for the ambushers.", "stats": {"AGI": 3, "INT": 2}},
            {"text": "You carry them on your back through the blizzard to safety.", "stats": {"STR": 3, "END": 2}},
        ]
    },
    {
        "id": 4,
        "label": "Scene IV \u2014 The Forbidden Archive",
        "title": "Ink and Dust",
        "narrative": "Deep beneath the city, you find an archive of forbidden knowledge. A guardian warns you: 'What you read here cannot be unlearned. Some truths break the mind.'",
        "question": "What do you choose?",
        "choices": [
            {"text": "You read everything. Knowledge is never the enemy.", "stats": {"INT": 3, "WIL": 2}},
            {"text": "You take only what you need and leave the rest sealed.", "stats": {"WIL": 3, "INT": 2}},
            {"text": "You copy the index and sell the location to the highest bidder.", "stats": {"CHA": 3, "AGI": 2}},
            {"text": "You destroy the archive. Some things should stay buried.", "stats": {"STR": 3, "WIL": 2}},
        ]
    },
    {
        "id": 5,
        "label": "Scene V \u2014 The Long March",
        "title": "Iron Will",
        "narrative": "Your group has been marching for three days without rest. Supplies are low. Morale is lower. Someone needs to keep everyone moving or you all die here.",
        "question": "How do you lead?",
        "choices": [
            {"text": "You take the heaviest pack and march at the front. No words needed.", "stats": {"END": 3, "STR": 2}},
            {"text": "You ration supplies precisely and calculate the optimal route.", "stats": {"INT": 3, "END": 2}},
            {"text": "You tell stories and sing songs to keep spirits alive.", "stats": {"CHA": 3, "WIL": 2}},
            {"text": "You push forward alone to scout ahead and find shelter.", "stats": {"AGI": 3, "END": 2}},
        ]
    },
    {
        "id": 6,
        "label": "Scene VI \u2014 The Shadow\u2019s Offer",
        "title": "Temptation",
        "narrative": "A shadow appears in your dream. It offers you immense power \u2014 but at the cost of your strongest bond. 'Everyone has a price,' it whispers. 'What\u2019s yours?'",
        "question": "What do you say?",
        "choices": [
            {"text": "'Nothing. I\u2019ll earn my power the hard way.'", "stats": {"WIL": 3, "END": 2}},
            {"text": "'Show me the fine print first.'", "stats": {"INT": 3, "CHA": 2}},
            {"text": "'I\u2019ll take it \u2014 and find a way to break the deal later.'", "stats": {"AGI": 3, "INT": 2}},
            {"text": "You attack the shadow. Some offers are threats in disguise.", "stats": {"STR": 3, "AGI": 2}},
        ]
    },
    {
        "id": 7,
        "label": "Scene VII \u2014 The Final Gate",
        "title": "Who You Are",
        "narrative": "You stand at the final gate. Beyond it lies your purpose \u2014 but the gate demands one truth from you before it opens: who are you, really?",
        "question": "What is your truth?",
        "choices": [
            {"text": "'I am the wall that does not break.'", "stats": {"END": 3, "STR": 2}},
            {"text": "'I am the mind that sees what others miss.'", "stats": {"INT": 3, "WIL": 2}},
            {"text": "'I am the voice that moves people to act.'", "stats": {"CHA": 3, "INT": 2}},
            {"text": "'I am the blade that strikes before the storm.'", "stats": {"AGI": 3, "STR": 2}},
        ]
    },
]


CLASSES = [
    {"name": "Knight",    "archetype": "Grimward", "primary": "STR", "secondary": "END"},
    {"name": "Berserker", "archetype": "Grimward", "primary": "STR", "secondary": "AGI"},
    {"name": "Warden",    "archetype": "Grimward", "primary": "END", "secondary": "WIL"},
    {"name": "Ronin",     "archetype": "Grimward", "primary": "WIL", "secondary": "STR"},
    {"name": "Ninja",     "archetype": "Ashborne", "primary": "AGI", "secondary": "INT"},
    {"name": "Alchemist", "archetype": "Ashborne", "primary": "INT", "secondary": "WIL"},
    {"name": "Phantom",   "archetype": "Ashborne", "primary": "AGI", "secondary": "WIL"},
    {"name": "Oracle",    "archetype": "Ashborne", "primary": "INT", "secondary": "CHA"},
    {"name": "Sage",      "archetype": "Goldveil", "primary": "INT", "secondary": "CHA", "tiebreak_wil": True},
    {"name": "Bard",      "archetype": "Goldveil", "primary": "CHA", "secondary": "AGI"},
    {"name": "Paladin",   "archetype": "Goldveil", "primary": "WIL", "secondary": "CHA"},
    {"name": "Mystic",    "archetype": "Goldveil", "primary": "WIL", "secondary": "INT"},
]
