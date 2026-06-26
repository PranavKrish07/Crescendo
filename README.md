# `Crescendo` - Advanced Core Progression Architecture

`Crescendo` is an industrial-grade, full-stack, gamified workflow orchestration and programmatic accountability framework. It completely reimagines productivity architectures by binding transaction-driven quest structures, daily checking mechanics, and structured learning tracks to an immersive RPG-style state engine. Built using a strict decoupled model, the platform leverages a high-performance **Django REST API REST Engine** paired with a highly reactive, state-managed **Vite-React UI Layer**.

---

## 🏗️ System Architecture & Codebase Design

The repository is built on a decoupled client-server architecture. The server processes database transactions, attribute scaling logic, and time-gated streak parameters, while the frontend handles dynamic client-side caching, secure global authentication contexts, and modern interface mutations.

```
                      [ CLIENT LAYER ]
               Vite React SPA (State Cache)
                            │
               (Bearer JWT Authorization JSON)
                            ▼
               [ NETWORK INTERFACE LAYER ]
             Axios Route Interceptor Abstract
                            │
               (Asynchronous HTTP Network Line)
                            ▼
                      [ SERVER LAYER ]
            Django REST Gateway ViewSet Controls
                            │
       ┌────────────────────┴────────────────────┐
       ▼                                         ▼
[ AUTH APP ]                              [ DASHBOARD APP ]
Character Awakening Engine          Quest & SubTask Operations
Custom Auth Attributes Matrix       Signals Matrix & Modifier Service

```

---

## 🛠️ Monolithic Codebase Structural Breakdown

### 📁 Server Architecture (`/backend`)

* **`backend/settings.py`**: Configures global middleware boundaries, JWT lifecycle thresholds, server-side CORS permissions, and security parameters.
* **`authentication/models.py`**: Extends Django's user configuration framework to tracking RPG mechanics: character class definitions (`char_class`), active awakening status (`awakening_done`), specialized character profile trees (`archetype`), and stat matrices (`stat_agi`, `stat_cha`, etc.).
* **`dashboard/models.py`**: Enforces strict operational tracking models including `Quest` entities, dependency-mapped `SubTask` tracking records, dynamic profile checkpoints (`UserProfile`), and scalable roadmap tracking structures (`RoadmapTemplate`, `UserRoadmap`).
* **`dashboard/class_modifiers.py` & `services.py**`: Houses calculation systems that compute attribute evolution metrics, streak break calculations, and rule configurations (e.g., tracking caps like `days_at_aura_cap`).
* **`dashboard/signals.py`**: Implements specialized event-listeners that automatically execute calculations and state mutations following user database updates.
* **`seed_roadmaps.py`**: Database seeding mechanism used to populate core roadmap configurations across user tables.

### 📁 Client Architecture (`/frontend`)

* **`src/api/axios.js`**: Core HTTP networking engine configured with global interceptors to attach authorization payloads and handle connection errors securely.
* **`src/context/AuthContext.jsx`**: Global application state layer managing protected user data, persistent token refreshing, and initialization checks across the entire routing tree.
* **`src/api/` (`dashboard.js`, `awakening.js`)**: Encapsulates specific async requests using clean functional patterns to communicate with server endpoints.
* **`src/components/`**: Modular presentation layouts managing complex feature states:
* `CreateQuestModal.jsx`: Interface handling form validations for custom quest injections.
* `QuestList.jsx`: Real-time list manager tracking nested interactive data components.
* `RitualModal.jsx`: Time-sensitive panel tracking recurring accountability checkpoints.



---

## ⚡ Core Systems & Production Workflows

### 1. Character Awakening Pipeline

When an unawakened account connects to the system, it enters a strict registration loop managed by `authentication/awakening_data.py`. Users must select a character base class—mirroring the assets located at `frontend/src/images/class-emblems/` (**Alchemist**, **Berserker**, **Knight**, **Ninja**). The application processes payload constraints through specialized serializers, records values to fields on the database, and flips `awakening_done` to prevent system manipulation.

### 2. Quest Hierarchy Validation Logic

Quests are modeled as atomic database states capable of nesting multiple sub-components (`SubTask`). When mutating task parameters from the frontend (`QuestList.jsx`), data flows securely through asynchronous REST transactions. Serialization fields (`fields`, `read_only_fields`) act as strict boundary guards, ensuring cross-user access attempts are blocked at the server gate.

### 3. Automated Progression Engine

Progression scaling runs independently of client inputs. Changes to a user profile automatically activate specific pipeline workflows inside `dashboard/signals.py`:

* **Streak Metrics Validation**: Processes consecutive task completions (`consecutive_quest_completions`) and records exact date intervals (`last_checkin`, `last_streak_break_date`).
* **Stat Modification**: Leverages class scaling metrics in `class_modifiers.py` to evaluate overall attribute levels and handle cap parameters safely.

---

## 🚀 Environment Initialization Lifecycle

Follow these steps exactly to configure an isolated development mirror of this project locally:

### 📡 Server Installation Sequence

Ensure you have Python installed locally. Navigating into the backend root:

```bash
# Move into server deployment root
cd backend

# Create an isolated environment instance
python -m venv venv

# Activate active script container (Windows)
.\venv\Scripts\activate
# Activate active script container (Linux/macOS)
source venv/bin/activate

# Install exact dependency requirements
pip install -r requirements.txt

```

Create a production-safe local configuration manifest named `.env` inside the `/backend` directory:

```env
DEBUG=True
SECRET_KEY=your_production_safe_fallback_secret_string
ALLOWED_HOSTS=localhost,127.0.0.1

```

Perform system state alignment across database models:

```bash
# Execute environment migrations
python manage.py migrate

# Seed structural learning blueprints 
python manage.py shell < seed_roadmaps.py

# Launch development environment instance
python manage.py runserver

```

### 💻 Client Installation Sequence

Ensure you have Node.js installed locally. Open a parallel workspace root:

```bash
# Move into frontend configuration directory
cd frontend

# Install client package configurations
npm install

# Run Vite engine locally
npm run dev

Boss, the layout is configured and ready. Open  of talking about code loosely like an amateur candidate, we extracted the underlying structural maps (viewsets, modifiers, contexts, files) and mapped them directly into a clear blueprint. This format presents your project to founders and technical buyers as a verified, industrial systems engineer. Let's push this asset live.
