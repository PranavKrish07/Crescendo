# 🚀 Crescendo: Product Bible

**Transform your daily grind into an S-Rank adventure.**

Crescendo is a revolutionary, gamified productivity platform built with Django and React. It elevates the mundane, transforming real-world tasks into a structured, high-stakes RPG experience. Featuring custom leveling algorithms, unforgiving penalty systems, and AI-assisted quest generation, Crescendo doesn't just manage your tasks—it trains you to be better.

---

## 1. Core Philosophy & Design

### 1.1 The S-Rank Vision
At its heart, Crescendo asks a simple question: *What if life had a leveling system?* We built an architecture that enforces discipline through high-stakes gamification. The experience is designed to be punishing but rewarding, echoing the difficulty and satisfaction of climbing ranks in a competitive RPG.

### 1.2 Aesthetics & Archetypes
Upon "Awakening", users choose an archetype that globally alters the application's entire aesthetic, injecting custom glassmorphism glows and neon accents into their dashboard:
*   **Grimward**: Blood Red hues, aggressive and bold.
*   **Ashborne**: Deep Royal Purple, mysterious and profound.
*   **Goldveil**: Amber and Gold, regal and resilient.

---

## 2. The Progression Systems

### 2.1 Experience & Leveling
*   **Global Leveling**: Advancing your base level occurs by completing quests and earning Experience Points (XP).
*   **Exponential Scaling**: The XP threshold to reach the next level is calculated exponentially (`100 * (1.5 ^ (level - 1))`), ensuring that higher levels require monumental effort and consistent dedication.

### 2.2 The Aura System
Aura is the lifeblood of Crescendo. It serves as your primary progression resource, defense mechanism, and currency.
*   **Aura Caps**: Each Rank has a strict maximum Aura capacity (e.g., Rank E caps at 900, Rank S at 999,999).
*   **Penalties**: Failing quests or breaking streaks results in significant Aura loss. If Aura drops below specific thresholds, automatic Rank Demotion occurs.

### 2.3 Ranks & Ascension Rituals
Users progress from **Rank E** up to **Rank S**. Ranking up is a grueling trial, never handed out freely.
*   **Rank Demotion**: Fully automated. If your Aura falls below your rank's minimum threshold, you are demoted immediately.
*   **Rank-Up Rituals**: To ascend, users must first cap their Aura and maintain it without a single drop for a required number of consecutive days. After meeting this prerequisite, they must execute a time-locked "Rank-Up Ritual." Failing the ritual locks the user out of another attempt for 7 days.

---

## 3. The Discipline Engines

### 3.1 The Streak System (Duolingo-style)
Daily engagement is enforced through a brutal streak system.
*   **Check-ins**: Users must check in daily to maintain their streak.
*   **Streak Freezes**: Users are granted a limited number of "Streak Freezes" to protect their progress on rest days.
*   **Devastating Penalties**: If a user runs out of freezes, their streak breaks. If a streak is broken **5 or more times in a single month**, the system inflicts a massive Aura penalty based on the user's Rank, often resulting in immediate demotion.

### 3.2 Grand Roadmaps
*   **High Stakes Guided Growth**: Massive, predefined multi-step roadmaps designed to heavily boost specific character stats (Strength, Endurance, Agility, Intelligence, Charisma, Willpower).
*   **The Oath**: Registering for a roadmap requires pledging to a strict deadline. 
*   **Rewards & Punishments**: Completing the roadmap on time grants massive Aura and Growth Points (GP). Failing the deadline or abandoning the roadmap inflicts severe Aura penalties.
*   **Rank Limitations**: Lower ranks (E-B) can only undertake up to 3 roadmaps simultaneously. S-Rank users have unlimited slots.

---

## 4. Quests & Gemini AI Integration

### 4.1 Quest Mechanics
*   **Categorization**: Quests are tied to specific stats (e.g., a "Workout" quest might boost Strength).
*   **Dynamic Difficulty**: Difficulty (Easy, Medium, Hard) is automatically calculated based on the number of subtasks required to complete the quest.

### 4.2 Auto-Generated Subtasks via Gemini AI
Users simply provide a quest title, and Crescendo leverages the **Google Gemini 1.5 API** to instantly generate a comprehensive, step-by-step subtask checklist. This eliminates decision fatigue and provides a clear, actionable path to accomplish the overarching goal.

---

## 5. Technical Architecture

*   **Backend (The Server)**: 
    *   Python 3.13+ and Django 5.2.
    *   Django REST Framework for API endpoints.
    *   SQLite database (for development), housing robust custom User, Quest, and Roadmap models.
    *   Custom OTP-based email authentication for secure user registration and "Awakening".
*   **Frontend (The Client)**:
    *   React & Vite.
    *   Vanilla CSS with a heavy focus on modern UI/UX animations, transitions, and glassmorphism.
*   **AI Engine**: Google Generative AI (Gemini 1.5) integrated directly into the quest creation pipeline.

---

## 6. The Roadmap Ahead
*   **Currently Implemented**: Custom Leveling, Glassmorphism Frontend, Gemini AI Integration, Rank-Up Rituals, and Grand Roadmaps.
*   **Next Up**: Guild Systems, Co-op Tasks, and Boss Raids.
*   **Future Vision**: Global Leaderboards to pit the highest-ranking "S-Rank" players against one another in a battle of pure productivity.
