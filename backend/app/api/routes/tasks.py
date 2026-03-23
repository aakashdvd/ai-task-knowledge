from fastapi import APIRouter, Depends, Query, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_admin
from app.models import Task, User
from app.schemas.task import TaskCreate, TaskOut, TaskStatusUpdate
from app.services.logging_service import create_activity_log
from app.services.task_service import (
    build_task_query,
    create_task as create_task_record,
    get_task_for_user,
    update_task_status,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    task = create_task_record(db=db, payload=payload, admin_user=admin_user)

    create_activity_log(
        db=db,
        user_id=admin_user.id,
        action="TASK_CREATED",
        entity_type="task",
        entity_id=task.id,
        details={
            "assigned_to": task.assigned_to,
            "title": task.title,
            "status": task.status,
        },
    )

    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(
    status_filter: str | None = Query(None, alias="status"),
    assigned_to: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = build_task_query(
        current_user=current_user,
        status_filter=status_filter,
        assigned_to_filter=assigned_to,
    )
    tasks = db.execute(stmt).scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_for_user(db=db, task_id=task_id, current_user=current_user)
    return task


@router.patch("/{task_id}/status", response_model=TaskOut)
def patch_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_for_user(db=db, task_id=task_id, current_user=current_user)

    is_admin = current_user.role.name.lower() == "admin"
    if not is_admin and task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="User is not allowed to update this task",
        )

    updated_task = update_task_status(db=db, task=task, new_status=payload.status)

    create_activity_log( 
        db=db,
        user_id=current_user.id,
        action="TASK_UPDATED",
        entity_type="task",
        entity_id=updated_task.id,
        details={
            "new_status": updated_task.status,
            "assigned_to": updated_task.assigned_to,
            "title": updated_task.title,
        },
    )

    db.commit()
    db.refresh(updated_task)
    return updated_task