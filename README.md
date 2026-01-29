# 🚀 Crescendo - Gamify your life, One task at a time

**Crescendo** is a gamified productivity platform built with Django that transforms real-life tasks into a structured RPG experience. Unlike standard to-do lists, Crescendo uses a custom leveling engine and stat-based roadmaps to drive personal growth through "S-Rank" performance.

---

## ✨ Key Features

### 🎮 RPG Growth System

* **Global Leveling**: Advance through levels using a custom-built threshold algorithm.
* **Dynamic Ranking**: Progress from **Rank E** to **Rank S** across multiple mental and physical attributes based on your trophy count.
* **User Classes**: Complete an initial quiz to be assigned a class (e.g., Knight, Ninja, Alchemist) that shapes your aesthetic and progression journey.

### 🗺️ Predefined Stat Roadmaps

* **Guided Growth**: Users can accept predefined "Roadmaps" designed to boost specific stats like Intelligence (INT) or Strength (STR).
* **Unique User Progression**: Built on a template-to-instance architecture. While roadmaps are shared, every user's progress, task completion, and timing are completely isolated.
* **Automated Rewards**: Completing roadmaps dynamically awards both XP and Stat Trophies using backend reflection.

---

## 🛠️ Technical Stack

* **Backend**: Django 5.x (Python)
* **Security**: `python-dotenv` for environment variable management.
* **Static Files**: `WhiteNoise` for high-performance serving of Glassmorphism CSS in production.
* **Database**: SQLite (Development).
* **Frontend**: HTML5, CSS3 (Modern Glassmorphism & Responsive Design).

---

## 🚀 Getting Started

### 1. Clone and Setup

```bash
git clone [Your Repo URL]
cd crescendo
pip install -r requirements.txt

```

### 2. Environment Variables

Create a `.env` file in the root directory and add your secrets:

```text
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

```

### 3. Initialize the Engine

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

```

### 4. Create an Admin & Launch

```bash
python manage.py createsuperuser
python manage.py runserver

```

*Login to `/admin` to populate your `StatQuests` and `StatTasks` templates.*

---

## 📅 Roadmap to S-Rank

* [x] Custom Leveling and XP Logic.
* [x] Production-ready Security & Static File Handling.
* [x] Responsive User Dashboard & Profile Cards.
* [ ] Individual StatTask tracking for unique roadmap progression.
* [ ] Multiplayer Leaderboards & Social "Guilds".

---

**Developed by Pranav Krishna** *Aspiring Founder & Computer Science Student*
