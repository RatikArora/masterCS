<div align="center">

# 🎓 MasterCS

### *Adaptive Learning Platform for GATE Exam Preparation*

**Duolingo meets LeetCode** — concept-first learning with spaced repetition, gamification, and intelligent question selection.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) · [Getting Started](#-getting-started) · [Architecture](#-architecture) · [API](#-api-endpoints) · [Contributing](#-contributing)

</div>

---

## 📸 Screenshots

<div align="center">
<table>
<tr>
<td><img src="https://github.com/RatikArora/masterCS/blob/main/docs/screenshots/dashboard.png?raw=true" width="400" alt="Dashboard" /><br/><b>Dashboard</b></td>
<td><img src="https://github.com/RatikArora/masterCS/blob/main/docs/screenshots/learn.png?raw=true" width="400" alt="Learn Page" /><br/><b>Adaptive Learning</b></td>
</tr>
<tr>
<td><img src="https://github.com/RatikArora/masterCS/blob/main/docs/screenshots/progress.png?raw=true" width="400" alt="Progress Analytics" /><br/><b>Progress Analytics</b></td>
<td><img src="https://github.com/RatikArora/masterCS/blob/main/docs/screenshots/badges.png?raw=true" width="400" alt="Badges & Achievements" /><br/><b>Badges & Achievements</b></td>
</tr>
</table>
</div>

---

## ✨ Features

### 🧠 Adaptive Question Algorithm

A multi-factor scoring engine that picks the *right* question at the *right* time:

| Factor | Weight | What it does |
|--------|--------|--------------|
| Wrong-answer urgency | 50 | Previously failed questions resurface first |
| Concept weakness | 15 | Low-confidence concepts get prioritized |
| Spaced repetition overdue | 20 | Past-due reviews bubble up |
| Novelty | 10 | Unseen concepts get introduced gradually |
| Difficulty match | 5 | Questions adapt to your skill level |
| Recency penalty | −2 | Avoids repeating questions you just saw |

Top-scored questions are selected via **weighted random sampling** from the top 5 candidates — structured yet unpredictable.

### 🔄 Spaced Repetition (SM-2 Variant)

Review intervals adapt based on performance *and* response speed:

- ✅ Correct → intervals grow: **1d → 3d → n × ease_factor** (max 120 days)
- ❌ Wrong → intervals shrink based on error streak severity
- ⚡ Fast answer → ease factor increases (strong recall)
- 🐢 Slow answer → ease factor decreases (shaky knowledge)

### 🏆 Gamification

| System | Details |
|--------|---------|
| **XP** | Easy=10, Medium=20, Hard=35 per correct answer |
| **Levels** | 10 tiers: Beginner → Novice → Learner → ... → Mythic (12K XP) |
| **Badges** | 21 achievements across XP, streaks, volume, mastery, and accuracy |
| **Hot Streaks** | Consecutive correct answers: 3→Hot, 5→On Fire, 10→Unstoppable, 20→**GODLIKE** |
| **Daily Streaks** | Track daily practice consistency with streak counters |
| **Sound Effects** | Audio feedback for correct/incorrect answers |

### 📚 Concept-First Learning

```
Learn concepts → Recognize patterns → Practice → Reflect → Revisit
```

- **Lesson Cards** — when you answer wrong, a concept review card explains the underlying theory
- **Wrong Question Reinforcement** — missed questions keep reappearing until mastered, then permanently excluded
- **5 Mastery Levels** — Novice → Learning → Familiar → Proficient → Mastered

### 📊 Progress Analytics

- Subject-wise accuracy & mastery distribution
- Topic-level progress breakdown
- Weak area identification (low confidence + high error rate)
- 30-day daily activity heatmap
- Streak tracking (current + longest)

### 🎯 Degree-Based Filtering

- **B.Tech** students → Computer Science subjects
- **B.Arch** students → Architecture & Planning subjects

---

## 📦 Content Library

| Subject | Questions | Topics | Coverage |
|---------|-----------|--------|----------|
| Computer Networks | 252 | 10 | OSI Model, TCP/IP, Routing, Subnetting, DNS, HTTP, and more |
| Architecture & Planning | 220+ | 22+ | Building Materials, Structural Systems, Urban Planning, Climate Design |
| **Total** | **472+** | **32+** | |

All questions include explanations, difficulty ratings (1–3), and estimated solve times.

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+
- **MySQL** 9.x
- **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/RatikArora/masterCS.git
cd masterCS
```

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up MySQL database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS mastercs;"

# Seed the database (run the app once — tables auto-create)
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → opens at http://localhost:5173
```

### Environment

The backend expects a local MySQL instance at `mysql+pymysql://root@localhost/mastercs`. To customize, edit `backend/app/config.py`.

---

## 🏗 Architecture

```
masterCS/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py             # App factory + CORS + startup
│   │   ├── config.py           # Settings (DB, JWT, thresholds)
│   │   ├── api/routes/         # Route handlers
│   │   │   ├── auth.py         #   Authentication (6 endpoints)
│   │   │   ├── concepts.py     #   Subjects, topics, concepts (4)
│   │   │   ├── learning.py     #   Adaptive questions + answers (4)
│   │   │   ├── progress.py     #   Analytics + streaks (5)
│   │   │   └── badges.py       #   Achievements (1)
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Core business logic
│   │   │   ├── question_selector.py   # ⭐ Adaptive algorithm
│   │   │   ├── spaced_repetition.py   # ⭐ SM-2 variant
│   │   │   ├── mastery_tracker.py     # Progress + XP + gamification
│   │   │   └── learning_engine.py     # Orchestrator
│   │   └── db/                 # Database seeds (472+ questions)
│   └── requirements.txt
│
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── api/                # Typed API client layer (Axios)
│   │   ├── store/              # Zustand state management
│   │   ├── pages/              # Route-level components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── LearnPage.tsx
│   │   │   ├── TopicBrowser.tsx
│   │   │   ├── ProgressPage.tsx
│   │   │   ├── BadgesPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── components/         # Reusable UI components
│   │   └── App.tsx             # Router + route guards
│   ├── package.json
│   └── vite.config.ts
│
└── arch/                       # GATE previous year papers (PDFs)
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI · SQLAlchemy · PyMySQL · Pydantic |
| **Auth** | JWT (python-jose) · bcrypt (passlib) |
| **Database** | MySQL 9.x |
| **Frontend** | React 19 · TypeScript · Vite 8 |
| **Styling** | Tailwind CSS 4 · Framer Motion |
| **State** | Zustand |
| **HTTP Client** | Axios |

---

## 🔌 API Endpoints

### Authentication — `/api/auth`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Create account |
| `POST` | `/login` | Get JWT token |
| `GET` | `/me` | Current user profile |
| `PATCH` | `/profile` | Update profile |
| `POST` | `/reset-progress/{subject_id}` | Reset subject progress |
| `POST` | `/reset-topic/{topic_id}` | Reset topic progress |

### Concepts — `/api/concepts`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/subjects` | List subjects (degree-filtered) |
| `GET` | `/subjects/{id}/topics` | Topics with concept counts |
| `GET` | `/topics/{id}/concepts` | Concepts with mastery progress |
| `GET` | `/concept/{id}` | Concept detail + statistics |

### Learning — `/api/learn`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/next-question/{subject_id}` | Get next adaptive question |
| `POST` | `/submit-answer` | Submit answer → feedback + XP |
| `GET` | `/wrong-questions/{subject_id}` | List incorrectly answered questions |
| `GET` | `/concept-notes/{concept_id}` | Concept explanation (lesson card) |

### Progress — `/api/progress`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/overview/{subject_id}` | Mastery distribution + accuracy |
| `GET` | `/topics/{subject_id}` | Per-topic breakdown |
| `GET` | `/weak-areas/{subject_id}` | Weak concepts |
| `GET` | `/daily-stats` | Last 30 days activity |
| `GET` | `/streak` | Current + longest streak |

### Badges — `/api/badges`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Badges, level, achievement progress |

### Health — `/api/health`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | System health check |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repo
2. **Create** a feature branch (`git checkout -b feat/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feat/amazing-feature`)
5. **Open** a Pull Request

### Guidelines

- Follow existing code style and project structure
- Write descriptive commit messages
- Add tests for new features when applicable
- Update documentation for API or schema changes

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️**

[⬆ Back to top](#-mastercs)

</div>
