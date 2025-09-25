from pydantic import BaseModel, ConfigDict, Field


class TaskAdd(BaseModel):
    name: str = Field(max_length=40)
    description: str | None = Field(None, max_length=60)


class Task(TaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskId(BaseModel):
    status: str = "ok"
    task_id: int