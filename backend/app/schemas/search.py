from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=10)


class SearchResultOut(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    score: float
    text: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResultOut]
    answer: str | None = None