# MasterCS — Copilot Instructions

## Project Overview
MasterCS is a Duolingo-style adaptive learning platform for Computer Science and Architecture students preparing for GATE exams. It uses spaced repetition (SM-2), adaptive difficulty scaling, weakness targeting, and a premium mobile-first UI.

## Tech Stack
- **Backend**: FastAPI (Python 3.13) + MySQL 9.x + SQLAlchemy ORM
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS v4 + Framer Motion
- **Auth**: JWT (bcrypt password hashing, stored in localStorage)
- **State**: Zustand (frontend), SQLAlchemy sessions (backend)

## Architecture

### Backend (`/backend/app/`)
```
app/
├── api/routes/          # FastAPI endpoints (auth, concepts, learning, progress)
├── core/                # Config, pagination, auth dependencies
├── db/                  # Database session, base model, seed scripts
├── models/              # SQLAlchemy ORM models (user, subject, concept, question, progress)
├── schemas/             # Pydantic request/response schemas
├── services/            # Business logic (learning_engine, question_selector, mastery_tracker)
└── main.py              # FastAPI app entry point
```

### Frontend (`/frontend/src/`)
```
src/
├── api/                 # Axios API client + typed endpoints
├── components/          # Reusable UI components (layout, learning, progress, ui)
├── pages/               # Route pages (Dashboard, LearnPage, TopicBrowser, ProgressPage)
├── store/               # Zustand stores (auth, learning)
├── App.tsx              # Router + route guards
└── main.tsx             # Entry point
```

## Core System: Learning Engine

### Question Selection (`question_selector.py`)
The brain of the system. Weighted random selection:
- 20% previously wrong questions (not recently answered)
- 30% weak area concepts (low confidence or high error streak)
- 20% revision (spaced repetition due)
- 30% new concept progression (curriculum order)

Supports **concept-focused mode**: when `concept_id` is set, only picks questions for that concept with adaptive difficulty.

### Mastery Tracking (`mastery_tracker.py`)
- SM-2 spaced repetition: intervals grow 1d→3d→7d→14d→30d→60d→120d
- Response time as signal: fast correct (+bonus), slow correct (-penalty)
- Confidence score: exponential moving average
- Mastery levels: novice → learning → familiar → proficient → mastered
- XP system: Easy=10, Medium=20, Hard=35, +5 per streak

### Adaptive Difficulty
Rolling accuracy from last 20 answers:
- ≥80% → Hard questions
- 50-80% → Medium questions
- <50% → Easy questions

## Database Schema (MySQL)
- All IDs are UUID strings (`str(uuid.uuid4())`)
- Questions link to concepts via `question_concepts` junction table
- Questions do NOT have `subject_id` or `is_active` columns
- Chain: question → question_concepts → concepts → topics → subjects
- Indexes on all foreign keys and frequent query patterns

## Coding Standards
- **SOLID principles**: reusable components, clean separation of concerns
- **Minimal DB queries**: use JOINs, aggregations, avoid N+1
- **Paginated APIs**: all list endpoints use pagination
- **Database indexes**: all FK columns and frequently queried fields indexed
- **Mobile-first**: design for phone, expand to desktop
- **No emojis**: use SVG icons everywhere
- **TypeScript strict**: zero type errors
- **RichText**: questions/explanations support markdown (react-markdown + remark-gfm)

## Subjects
Currently supported:
1. **Computer Networks** (CS/GATE) — 10 topics, 36 concepts, 160+ questions
2. **Architecture & Planning** (GATE AR) — Being developed

## How to Run
```bash
# Backend
cd backend && pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend && npm install
npx vite --host

# Seed database
cd backend && python3 -c "from app.db.seed import seed_database; seed_database()"
```

## Database
```bash
mysql -u root mastercs  # No password needed (local dev)
```

## Key Design Decisions
1. Content is markdown-first — use tables, code blocks, bold for emphasis
2. Question cooldown: 4 hours (configurable)
3. Wrong questions re-enter the learning flow automatically
4. Concepts are clickable → focused learning mode
5. Progress uses weighted scoring (not binary mastered/not-mastered)
