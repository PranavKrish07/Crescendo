# 🚀 Crescendo - Gamify you life, One task at a time

**Crescendo** is a gamified productivity platform built with Django that transforms real-life tasks into a structured RPG experience. Unlike standard to-do lists, Crescendo uses a custom leveling engine and stat-based roadmaps to drive personal growth through "S-Rank" performance.

---

## ✨ Key Features

### 🎮 RPG Growth System

* **Global Leveling**: Advance through levels using a custom-built threshold algorithm: .
* **Dynamic Ranking**: Progress from **Rank E** to **Rank S** across multiple mental and physical attributes based on your trophy count.
* **User Classes**: Complete an initial quiz to be assigned a class (e.g., Knight, Ninja, Alchemist) that shapes your aesthetic and progression journey.

### 🗺️ Predefined Stat Roadmaps (New in V1)

* **Guided Growth**: Beyond manual tasks, users can now accept predefined "Roadmaps" designed to boost specific stats like Intelligence (INT) or Strength (STR).
* **Unique User Progression**: Built on a template-to-instance architecture. While roadmaps are shared, every user's progress, task completion, and timing are completely isolated and unique.
* **Automated Rewards**: Completing roadmaps dynamically awards both XP and Stat Trophies using efficient backend reflection (`getattr`/`setattr`).

### 📝 Task Management

* **Manual Quests**: Create custom "Lists" and "Tasks" for daily chores or projects.
* **Dynamic Difficulty**: Quests are automatically assigned a difficulty level (Simple to Extreme) based on the number of sub-tasks involved, scaling XP rewards accordingly.

---

## 🛠️ Technical Stack

* **Backend**: Django (Python 3.x)
* **Database**: SQLite (Development)
* **Frontend**: HTML5, CSS3 (Modern Glassmorphism & Responsive Design)
* **Authentication**: Custom User model with class-based profile extensions.

---

## 🏗️ Database Architecture

Crescendo V1 implements a robust relational structure to handle gamification at scale:

* **`StatQuest`**: The master template defining rewards and categories.
* **`StatTask`**: Predefined steps associated with a roadmap template.
* **`UserQuestProgress`**: The bridge model that tracks a specific user’s progress through a shared roadmap.
* **`User_profile`**: Stores the central "Game State" for each user, including levels, XP, and trophies across 8 distinct attributes.

---

## 🚀 Getting Started

1. **Clone the repository**:
```bash
git clone [Your Repo URL]

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Run Migrations**:
```bash
python manage.py makemigrations
python manage.py migrate

```


4. **Create a Superuser** (to add StatQuests via Admin):
```bash
python manage.py createsuperuser

```


5. **Launch the engine**:
```bash
python manage.py runserver

```



---

## 📅 Roadmap to S-Rank

* [x] Custom Leveling and XP Logic
* [x] Responsive User Dashboard & Profile Cards
* [x] Predefined Stat-Roadmap Engine
* [ ] Individual StatTask tracking for unique roadmap progression.
* [ ] Advanced CSS Refactoring & UI modularity.
* [ ] Multiplayer Leaderboards & Social "Guilds."

---

**Developed by Pranav Krishna** *Aspiring Founder & Computer Science Student*
