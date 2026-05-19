# Pure reasoning agent — no tools, just text in, text out.
# Temperature is kept very low because deduplication and credibility
# ranking should be deterministic, not creative.

from crewai import Agent, LLM
from config.settings import settings

_llm = LLM(
    model="anthropic/claude-haiku-4-5-20251001",
    api_key=settings.anthropic_api_key,
    temperature=0.1,
)


def get_analyst_agent() -> Agent:
    return Agent(
        role="Research Analyst",
        goal="Deduplicate information, rank insights by relevance, and flag low-credibility sources.",
        backstory=(
            "You are a meticulous research analyst. You take raw research notes and "
            "distill them into clear, ranked insights — removing duplicates, "
            "prioritizing the most credible and relevant findings, and flagging "
            "any sources that appear unreliable."
        ),
        llm=_llm,
        max_iter=3,
    )
