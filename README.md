# 🚀 Crescendo
livelink: https://crescendo-avdj.onrender.com/

**Transform your daily grind into an S-Rank adventure.** Crescendo is a gamified productivity platform built with Django that turns real-world tasks into a structured RPG experience, using custom leveling algorithms and stat-based progression.

---

## ✨ Key Features

### 🎮 RPG Growth System

* **Dynamic Class Assignment**: Complete an initial quiz to be assigned a unique class (Knight, Ninja, or Alchemist) that shapes your aesthetic journey.
* **Global Leveling**: Advance through levels using a custom-built threshold algorithm.
* **Attribute Ranking**: Progress from **Rank E** to **Rank S** across mental and physical attributes based on trophy counts.

### 🗺️ Stat-Driven Roadmaps

* **Guided Growth**: Accept predefined "Roadmaps" designed to boost specific stats like Intelligence (INT) or Strength (STR).
* **Template-to-Instance Architecture**: Roadmaps are shared templates, but every user's progress and task timing remain completely isolated.
* **Automated Rewards**: XP and Stat Trophies are dynamically awarded upon completion using backend reflection.

---

## 🛠️ Technical Stack

* **Core**: Python 3.13+, Django 5.2.
* **Database**: SQLite (Development).
* **Production Serving**: WhiteNoise for high-performance static file delivery and Gunicorn as the WSGI server.
* **Frontend**: Modern Glassmorphism CSS with responsive HTML5.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pranavkrish07/crescendo.git
cd crescendo

```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```text
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

```

### 3. Initialize the Engine

The project includes a `build.sh` script for automated deployment, but for local setup, run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver

```

---

## 📅 Roadmap to S-Rank

* [x] Custom Leveling and XP Logic.
* [x] Production-ready Security & Static File Handling.
* [x] Responsive User Dashboard & Profile Cards.
* [ ] **Next Up**: Individual StatTask tracking for unique roadmap progression.
* [ ] **Future**: Multiplayer Leaderboards & Social "Guilds".

##Screenshots 
---


## 👤 Author

**Pranav Krishna** *Aspiring Founder & Computer Science Student*.
