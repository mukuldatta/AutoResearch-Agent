import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ResearchRequest, ResearchResult
from crew import run_research_crew

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AutoResearch Agent")

# Wide-open CORS is fine for local development. If you deploy this anywhere
# public, lock allow_origins down to your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.post("/research", response_model=ResearchResult)
def research(request: ResearchRequest):
    try:
        report = run_research_crew(request.query)
        return ResearchResult(report=report)
    except Exception as e:
        # Log the full trace internally but send a clean message to the client —
        # raw CrewAI / LLM errors can leak API details you don't want exposed.
        logger.error("Research pipeline failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Research pipeline failed. Please try again.")
