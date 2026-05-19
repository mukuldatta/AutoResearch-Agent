# The researcher is the only agent with a tool. It runs one Tavily search
# per subtopic, so max_iter is higher than the other agents to give it room
# to make multiple tool calls without hitting the iteration cap.

from crewai import Agent, LLM
from config.settings import settings
from tools.tavily_tool import TavilySearchTool

_llm = LLM(
    model="anthropic/claude-haiku-4-5-20251001",
    api_key=settings.anthropic_api_key,
    temperature=0.3,
)

# Tool instance is shared — TavilySearchTool holds no per-request state.
_tool = TavilySearchTool()


def get_researcher_agent() -> Agent:
    return Agent(
        role="Web Researcher",
        goal="For each subtopic, search the web and collect raw facts, quotes, and source URLs.",
        backstory=(
            "You are a skilled web researcher. Given a list of subtopics, you search "
            "the web thoroughly for each one and gather relevant facts, statistics, "
            "quotes, and URLs to build a solid evidence base."
        ),
        llm=_llm,
        tools=[_tool],
        max_iter=5,  # Needs up to one search call per subtopic (3-5 subtopics)
    )
