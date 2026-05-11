from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


Priority = Literal["low", "medium", "high"]


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority = "medium"
    email: EmailStr | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: Priority | None = None


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    priority: Priority
    attachment: str | None
    email: EmailStr | None
    created_at: datetime
    updated_at: datetime | None = None
