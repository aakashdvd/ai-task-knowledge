from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import SearchLog, User
from app.services.embedding_service import search_similar_chunks
from app.services.logging_service import create_activity_log


def execute_search(
    db: Session,
    current_user: User,
    query: str,
    top_k: int,
) -> list[dict]:
    raw_results = search_similar_chunks(query=query, top_k=top_k)

    filtered_results: list[dict] = []
    for item in raw_results:
        if item["distance"] <= settings.SEARCH_DISTANCE_THRESHOLD:
            filtered_results.append(
                {
                    "document_id": item["document_id"],
                    "filename": item["filename"],
                    "chunk_index": item["chunk_index"],
                    "score": item["score"],
                    "text": item["text"],
                }
            )

    search_log = SearchLog(
        user_id=current_user.id,
        query_text=query,
        results_count=len(filtered_results),
    )
    db.add(search_log)
    db.flush()

    create_activity_log(
        db=db,
        user_id=current_user.id,
        action="SEARCH_EXECUTED",
        entity_type="search",
        entity_id=search_log.id,
        details={
            "query": query,
            "results_count": len(filtered_results),
            "top_k": top_k,
            "distance_threshold": settings.SEARCH_DISTANCE_THRESHOLD,
        },
    )

    return filtered_results