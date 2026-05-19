# Temperature is slightly higher here than the other agents. A bit of
# variance in prose makes the output feel less robotic without sacrificing
# the structured format enforced by the task's expected_output.

from crewai import Agent, LLM
from config.settings import settings

_llm = LLM(
    model="anthropic/claude-haiku-4-5-20251001",
    api_key=settings.anthropic_api_key,
    temperature=0.5,
)


def get_writer_agent() -> Agent:
    return Agent(
        role="Report Writer",
        goal="Produce a structured markdown report with Executive Summary, per-subtopic sections, key takeaways, and a Sources section.",
        backstory=(
            "You are an expert technical writer. You take curated research insights "
            "and craft them into a well-structured, readable markdown report with "
            "an executive summary, detailed sections per subtopic, key takeaways, "
            "and a properly formatted sources section."
        ),
        llm=_llm,
        max_iter=3,
    )
