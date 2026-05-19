# AutoResearch Agent

An AI-powered research automation system that orchestrates four specialized agents — planner, researcher, analyst, and writer — to produce a structured, fully-sourced markdown report on any topic.

## How it works

```
User query (Streamlit UI)
    │
    ▼
FastAPI /research endpoint
    │
    ▼
CrewAI sequential pipeline
    ├─ Planner   → decomposes query into 3-5 subtopics
    ├─ Researcher → web-searches each subtopic via Tavily
    ├─ Analyst   → deduplicates, ranks, flags low-credibility sources
    └─ Writer    → produces a structured markdown report
    │
    ▼
Report rendered in Streamlit
```

Each agent is powered by **Claude Haiku 4.5**. Web search is handled by the **Tavily API**.

## Output format

Every report includes:
- **Executive Summary** — top-level overview
- **Per-subtopic sections** — detailed findings with inline source attribution
- **Key Takeaways** — distilled conclusions
- **Sources** — numbered markdown links to every URL found during research

## Project structure

```
autoreasarch-agent/
├── backend/
│   ├── agents/
│   │   ├── planner.py      # breaks query into subtopics
│   │   ├── researcher.py   # web search + fact collection
│   │   ├── analyst.py      # deduplication + credibility ranking
│   │   └── writer.py       # markdown report generation
│   ├── tools/
│   │   └── tavily_tool.py  # CrewAI tool wrapping Tavily search
│   ├── config/
│   │   └── settings.py     # env var management via pydantic-settings
│   ├── crew.py             # pipeline orchestration
│   ├── main.py             # FastAPI app
│   └── schemas.py          # request/response models
├── frontend/
│   └── app.py              # Streamlit UI
├── .env.example
└── requirements.txt
```

## Prerequisites

- Python 3.12+
- An [Anthropic API key](https://console.anthropic.com/)
- A [Tavily API key](https://tavily.com/)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/autoreasarch-agent.git
cd autoreasarch-agent

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in your API keys
```

## Running

Open two terminals from the project root.

**Terminal 1 — backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 — frontend:**
```bash
cd frontend
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Claude Haiku 4.5 (Anthropic) |
| Multi-agent framework | CrewAI |
| Web search | Tavily |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Config | pydantic-settings |

## Environment variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |
| `TAVILY_API_KEY` | Tavily API key for web search |

Copy `.env.example` to `.env` and fill in your keys. **Never commit `.env`** — it is listed in `.gitignore`.
