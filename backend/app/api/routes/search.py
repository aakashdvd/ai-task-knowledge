from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import User
from app.schemas.search import SearchRequest, SearchResponse, SearchResultOut
from app.services.gemini_service import generate_grounded_answer
from app.services.search_service import execute_search

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("", response_model=SearchResponse)
def search_documents(
    payload: SearchRequest,
    include_answer: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = execute_search(
        db=db,
        current_user=current_user,
        query=payload.query,
        top_k=payload.top_k,
    )

    answer = generate_grounded_answer(payload.query, results) if include_answer else None

    db.commit()

    return SearchResponse(
        query=payload.query,
        results=[SearchResultOut(**item) for item in results],
        answer=answer,
    )