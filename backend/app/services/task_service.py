from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models import Task, User
from app.schemas.task import TaskCreate


def build_task_query(
    current_user: User,
    status_filter: str | None = None,
    assigned_to_filter: int | None = None,
) -> Select[tuple[Task]]:
    stmt = select(Task)

    if current_user.role.name.lower() == "admin":
        if status_filter:
            stmt = stmt.where(Task.status == status_filter)
        if assigned_to_filter:
            stmt = stmt.where(Task.assigned_to == assigned_to_filter)
    else:
        stmt = stmt.where(Task.assigned_to == current_user.id)
        if status_filter:
            stmt = stmt.where(Task.status == status_filter)

    stmt = stmt.order_by(Task.created_at.desc())
    return stmt


def create_task(db: Session, payload: TaskCreate, admin_user: User) -> Task:
    assignee = db.execute(
        select(User).where(User.id == payload.assigned_to, User.is_active.is_(True))
    ).scalars().first()

    if not assignee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found",
        )

    task = Task(
        assigned_by=admin_user.id,
        assigned_to=payload.assigned_to,
        title=payload.title.strip(),
        description=payload.description.strip() if payload.description else None,
        due_date=payload.due_date,
        status="pending",
    )
    db.add(task)
    db.flush()
    return task


def get_task_for_user(db: Session, task_id: int, current_user: User) -> Task:
    stmt = select(Task).where(Task.id == task_id)
    task = db.execute(stmt).scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    is_admin = current_user.role.name.lower() == "admin"
    if not is_admin and task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this task",
        )

    return task


def update_task_status(db: Session, task: Task, new_status: str) -> Task:
    if task.status == new_status:
        return task

    if new_status not in {"pending", "completed"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task status",
        )

    if task.status == "completed" and new_status == "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completed task cannot be moved back to pending in this MVP",
        )

    task.status = new_status

    if new_status == "completed":
        task.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.add(task)
    db.flush()
    return task