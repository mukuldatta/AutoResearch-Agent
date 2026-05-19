# Orchestrates the four-agent pipeline in a fixed sequence.
# Each task passes its output as context to the next, so the writer
# always has the full research history — not just the analyst's summary.

from crewai import Crew, Task, Process
from agents.planner import get_planner_agent
from agents.analyst import get_analyst_agent
from agents.researcher import get_researcher_agent
from agents.writer import get_writer_agent


def run_research_crew(query: str) -> str:
    # Fresh agent instances per request — CrewAI agents track internal
    # iteration state, so reusing them across calls causes subtle bugs.
    planner = get_planner_agent()
    researcher = get_researcher_agent()
    analyst = get_analyst_agent()
    writer = get_writer_agent()

    plan_task = Task(
        description=f"Decompose the following research query into 3-5 focused subtopics:\n\n{query}",
        expected_output="A numbered list of 3-5 specific, non-overlapping subtopics to research.",
        agent=planner,
    )

    research_task = Task(
        description="For each subtopic from the planner, search the web and collect facts, quotes, and source URLs. You MUST include the full URL for every source you find.",
        expected_output="Raw research notes, one block per subtopic. Each block must list the source URL on its own line prefixed with 'Source:'.",
        agent=researcher,
        context=[plan_task],
    )

    analysis_task = Task(
        description="Deduplicate the research notes, rank insights by relevance, and flag low-credibility sources.",
        expected_output="Curated bullet-point insights with source attribution.",
        agent=analyst,
        context=[research_task],
    )

    # Writer gets both research and analysis context. Without research_task here,
    # URLs the analyst chose not to highlight would be silently dropped from
    # the final Sources section.
    writing_task = Task(
        description="Write a structured markdown research report based on the curated insights. You MUST end the report with a '## Sources' section that lists every URL collected during research as a numbered markdown link.",
        expected_output="A complete markdown report with: ## Executive Summary, one ## section per subtopic, ## Key Takeaways, and ## Sources with all URLs as numbered markdown links [Title](URL).",
        agent=writer,
        context=[research_task, analysis_task],
    )

    crew = Crew(
        agents=[planner, researcher, analyst, writer],
        tasks=[plan_task, research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=False,
    )

    return str(crew.kickoff())
