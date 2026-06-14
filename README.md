# AI Health Coach — Maya

A conversational AI wellness coaching assistant built with Python, Streamlit, LangChain, ChromaDB, and OpenAI.

> **Disclaimer:** This app provides general wellness and lifestyle coaching only.
> It is **not** a medical service and does not diagnose, treat, or replace professional healthcare.
> Always consult a qualified healthcare provider for medical concerns.

---

## Overview

Maya is an AI-powered health coach that helps users build healthier habits through personalized, evidence-based wellness guidance. It combines a Retrieval-Augmented Generation (RAG) pipeline over curated health coaching documents with a conversational LLM interface — demonstrating real-world LLM application patterns in a clean, beginner-friendly codebase.

**Coaching areas:** nutrition, sleep, stress management, habit formation, movement, and general lifestyle.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Onboarding  │  │  Chat UI     │  │   Sidebar     │  │
│  │  (form)     │  │  (messages)  │  │  (profile +   │  │
│  └──────┬──────┘  └──────┬───────┘  │   actions)    │  │
│         │                │          └───────────────┘  │
└─────────┼────────────────┼───────────────────────────--┘
          │                │
          ▼                ▼
┌─────────────────┐  ┌─────────────────────────────────────┐
│    SQLite DB    │  │           HealthCoach               │
│  (user profile) │  │                                     │
│  utils/db.py    │  │  1. Safety Check (core/safety.py)   │
└─────────────────┘  │     └─ medical? → guardrail msg     │
                     │     └─ emergency? → 911 redirect    │
                     │  2. RAG Retrieval (core/rag.py)     │
                     │     └─ ChromaDB similarity search   │
                     │  3. LLM Call (ChatOpenAI)           │
                     │     └─ system prompt + user profile │
                     │        + RAG context + history      │
                     └─────────────────────────────────────┘
                                      │
                     ┌────────────────┴────────────────────┐
                     │                                     │
              ┌──────▼──────┐                  ┌──────────▼──────┐
              │  ChromaDB   │                  │   OpenAI API    │
              │  (local)    │                  │  gpt-4o-mini    │
              │  data/      │                  └─────────────────┘
              │  chroma_db/ │
              └─────────────┘
                     ▲
              ┌──────┴──────┐
              │  Knowledge  │
              │  Documents  │
              │  data/      │
              │  knowledge/ │
              └─────────────┘
```

---

## Features

- **Personalized onboarding** — name, goal, dietary preference, sleep, stress, movement, health concerns
- **Conversational coaching** — streaming chat with session memory, reflective questions, habit suggestions
- **RAG knowledge base** — 5 expert health coaching documents indexed in ChromaDB
- **7-day wellness plan generator** — personalized to the user's profile and goals
- **Meal ideas** — tailored to dietary preference and goal (not a medical diet plan)
- **Safety guardrails** — automatic detection of medical/emergency queries → appropriate redirect
- **User profile persistence** — SQLite; profile survives page refresh

---

## Folder Structure

```
ai-health-coach/
├── main.py                         # Streamlit entry point
├── app/
│   ├── onboarding.py               # User profile form
│   ├── chat.py                     # Chat interface + message rendering
│   └── sidebar.py                  # Sidebar with profile + quick actions
├── core/
│   ├── prompts.py                  # System prompt + plan/meal templates
│   ├── safety.py                   # Medical and emergency guardrails
│   ├── rag.py                      # ChromaDB RAG pipeline
│   └── coach.py                    # LLM orchestrator (streaming + special actions)
├── models/
│   └── user_profile.py             # UserProfile dataclass
├── utils/
│   └── db.py                       # SQLite persistence helpers
├── data/
│   ├── knowledge/                  # Health coaching documents (.md)
│   │   ├── nutrition_basics.md
│   │   ├── sleep_hygiene.md
│   │   ├── stress_management.md
│   │   ├── habit_formation.md
│   │   └── exercise_guidelines.md
│   └── chroma_db/                  # Auto-created vector store (gitignored)
├── .env.example                    # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd ai-health-coach
```

### 2. Create a virtual environment

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
```

> `gpt-4o-mini` is recommended for portfolio/demo use — it's cost-effective and high quality.

### 5. Run the app

```bash
streamlit run main.py
```

The knowledge base will be indexed on first launch (takes ~10–20 seconds, only once).
Subsequent launches load from the persisted ChromaDB.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | OpenAI GPT-4o-mini via LangChain |
| RAG | LangChain + ChromaDB |
| Embeddings | OpenAI text-embedding-3-small |
| User persistence | SQLite |
| Environment | python-dotenv |

---

## Safety Design

The safety module (`core/safety.py`) intercepts messages before they reach the LLM:

- **Emergency patterns** (chest pain, breathing difficulty, suicidal ideation) → immediate 911/crisis line redirect
- **Medical patterns** (symptoms, medications, diagnoses, dosages) → warm redirect to appropriate professionals

The system prompt reinforces these boundaries for all other queries.

---

## Extending the Knowledge Base

Add any `.md` or `.txt` files to `data/knowledge/`. Delete `data/chroma_db/` to force a re-index on next launch.

---

## Screenshots

_Add screenshots here once the app is running_

| Onboarding | Chat | Wellness Plan |
|---|---|---|
| ![onboarding](screenshots/onboarding.png) | ![chat](screenshots/chat.png) | ![plan](screenshots/plan.png) |

---

## Portfolio Notes

This project demonstrates:
- **RAG pattern** — document loading → chunking → embedding → semantic retrieval → prompt injection
- **Prompt engineering** — persona, constraints, dynamic user context, safety instructions
- **Streaming LLM output** — token-by-token display using LangChain streaming
- **Layered architecture** — clean separation of UI, orchestration, RAG, safety, and data layers
- **Safety-first LLM design** — pre-LLM safety checks, medical boundary enforcement

---

## License

MIT
