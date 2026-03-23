from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TaskStatus = Literal["pending", "completed"]


class TaskCreate(BaseModel):
    assigned_to: int
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = None
    due_date: datetime | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assigned_by: int
    assigned_to: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime