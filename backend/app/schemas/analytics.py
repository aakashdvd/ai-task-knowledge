from pydantic import BaseModel


class TopSearchOut(BaseModel):
    query_text: str
    count: int


class AnalyticsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    total_documents: int
    total_searches: int
    top_searches: list[TopSearchOut]