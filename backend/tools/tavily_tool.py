import asyncio
from crewai.tools import BaseTool
from tavily import TavilyClient
from config.settings import settings

# Lazily initialised so the client isn't created at import time.
# This avoids a hard failure during testing or if the key isn't set yet.
_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=settings.tavily_api_key)
    return _client


class TavilySearchTool(BaseTool):
    name: str = "tavily_search"
    description: str = "Search the web for information on a given topic. Input should be a search query string."

    def _run(self, query: str) -> str:
        # 5 results per subtopic gives enough variety without flooding the
        # context window. 3 was too sparse for niche or technical queries.
        results = _get_client().search(query=query, max_results=5)
        output = []
        for r in results.get("results", []):
            output.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n")
        return "\n---\n".join(output) if output else "No results found."

    async def _arun(self, query: str) -> str:
        # TavilyClient is synchronous, so we push it to a thread rather than
        # calling _run() directly, which would block the event loop.
        return await asyncio.to_thread(self._run, query)
