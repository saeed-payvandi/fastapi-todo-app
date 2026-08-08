from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=5, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    is_compleated: bool = Field(..., description="State of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")

    created_date: datetime = Field(..., description="Creation date and time of the object")
    updated_date: datetime = Field(..., description="Updating date and time of the object")
    