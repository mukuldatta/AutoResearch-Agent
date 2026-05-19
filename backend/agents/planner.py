# The planner just needs to split a question into subtopics — no tools,
# no creativity required. Temperature 0.3 keeps it focused and consistent.

from crewai import Agent, LLM
from config.settings import settings

# LLM is created once at module load and shared across all requests.
# CrewAI's LLM wrapper is stateless between calls, so this is safe.
_llm = LLM(
    model="anthropic/claude-haiku-4-5-20251001",
    api_key=settings.anthropic_api_key,
    temperature=0.3,
)


def get_planner_agent() -> Agent:
    return Agent(
        role="Research Planner",
        goal="Decompose the user query into 3-5 focused, non-overlapping subtopics.",
        backstory=(
            "You are an expert research strategist. Given a broad research question, "
            "you break it down into clear, specific subtopics that together give a "
            "comprehensive picture of the subject."
        ),
        llm=_llm,
        max_iter=3,  # Planning rarely needs more than one pass
    )
