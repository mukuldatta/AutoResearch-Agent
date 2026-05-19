from pydantic import BaseModel, field_validator


class ResearchRequest(BaseModel):
    query: str

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Query must be at least 10 characters.")
        # 1000 chars is generous for a research question. Anything longer
        # is probably a copy-paste accident and would bloat the planner prompt.
        if len(v) > 1000:
            raise ValueError("Query must be at most 1000 characters.")
        return v


class ResearchResult(BaseModel):
    report: str
