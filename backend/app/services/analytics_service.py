from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models import Document, SearchLog, Task


def get_basic_analytics(db: Session) -> dict:
    total_tasks = db.scalar(select(func.count(Task.id))) or 0
    total_documents = db.scalar(select(func.count(Document.id))) or 0
    total_searches = db.scalar(select(func.count(SearchLog.id))) or 0

    status_rows = db.execute(
        select(Task.status, func.count(Task.id))
        .group_by(Task.status)
    ).all()

    completed_tasks = 0
    pending_tasks = 0

    for status, count in status_rows:
        if status == "completed":
            completed_tasks = count
        elif status == "pending":
            pending_tasks = count

    top_search_rows = db.execute(
        select(
            SearchLog.query_text,
            func.count(SearchLog.id).label("count"),
        )
        .group_by(SearchLog.query_text)
        .order_by(desc("count"), SearchLog.query_text.asc())
        .limit(10)
    ).all()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_documents": total_documents,
        "total_searches": total_searches,
        "top_searches": [
            {
                "query_text": row[0],
                "count": row[1],
            }
            for row in top_search_rows
        ],
    }