# 🚀 Crescendo

**Transform your daily grind into an S-Rank adventure.** 
Crescendo is a gamified productivity platform built with Django and React that turns real-world tasks into a structured RPG experience, complete with custom leveling algorithms, unforgiving penalty systems, and AI-assisted quest generation.

---

## ✨ Key Features

### 🎮 RPG Progression System
* **Global Leveling**: Advance your base level by completing quests, earning XP with an exponentially scaling threshold algorithm.
* **Aura Energy**: Your primary progression resource. Aura is required for everything and comes with a strict cap based on your rank.
* **The Streak System**: Duolingo-style daily check-ins. Maintain your streak to keep your Aura safe. Break your streak 5+ times in a month, and suffer devastating Aura penalties based on your rank.

### ⚔️ Archetypes & Aesthetics
* **Dynamic House Assignment**: Choose between **Grimward** (Red), **Ashborne** (Purple), or **Goldveil** (Amber). Your chosen archetype globally alters the app's entire aesthetic, injecting custom glassmorphism glows and neon accents into your dashboard.

### 🤖 Gemini AI Quests
* **Auto-Generated Subtasks**: Provide a quest title, and Crescendo uses the Google Gemini API to instantly generate a comprehensive, step-by-step checklist to help you accomplish your goal.

### 🗺️ Grand Roadmaps
* **High Stakes Guided Growth**: Register for massive predefined roadmaps designed to boost specific stats (Strength, Intelligence, Charisma, etc.). 
* **Growth Points (GP)**: Complete roadmaps to inject Growth Points directly into your stats.
* **The Oath**: Roadmaps require a strict deadline. Complete them in time for massive Aura and GP rewards. Fail them, or break your oath manually, and suffer severe Aura penalties. Registration is limited by your Rank (E-B ranks get 3 slots, S ranks get unlimited).

### 🔥 Rank-Up Rituals
* Progress from **Rank E** to **Rank S**. Ranking up is not handed to you. 
* To ascend, you must cap your Aura and sustain it for a set number of consecutive days without a single drop.
* Once the prerequisite is met, you must execute a "Rank-Up Ritual"—a grueling, time-locked trial. Fail the ritual, and you're locked out for 7 days.

---

## 🛠️ Technical Stack

* **Backend**: Python 3.13+, Django 5.2, Django REST Framework, SQLite (Development).
* **Frontend**: React, Vite, Vanilla CSS with heavy focus on Glassmorphism and modern UI/UX animations.
* **AI Integration**: Google Generative AI (Gemini 1.5).

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pranavkrish07/crescendo.git
cd crescendo
```

### 2. Backend Setup (Django)

Open a terminal and navigate to the `backend` directory:

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Run migrations to setup the database
python manage.py migrate

# Seed the database with the predefined Grand Roadmaps
python seed_roadmaps.py

# Create an admin account (optional)
python manage.py createsuperuser

# Start the Django API server
python manage.py runserver
```

### 3. Frontend Setup (React/Vite)

Open a **new** terminal and navigate to the `frontend` directory:

```bash
cd frontend
npm install

# Start the Vite development server
npm run dev
```

### 4. Gemini API Configuration
Crescendo uses Gemini to automatically generate subtasks for your quests.
1. Obtain an API key from Google AI Studio.
2. In the Crescendo Dashboard, click the "Gemini API" button in the navigation bar to securely save your key in your browser's local storage.

---

## 📅 Roadmap to S-Rank

* [x] Custom Leveling and XP Logic.
* [x] Glassmorphism React Frontend.
* [x] Gemini AI Task Generation.
* [x] Rank-Up Rituals and Aura Capping.
* [x] Grand Roadmaps implementation.
* [ ] **Next Up**: Guild Systems, Co-op Tasks, and Boss Raids.
* [ ] **Future**: Global Leaderboards.

---

## 👤 Author

**Pranav Krishna** *Aspiring Founder & Computer Science Student*.
