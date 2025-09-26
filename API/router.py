from fastapi import APIRouter, Depends
from typing import Annotated
from repository import TaskRepository
from schemas import Task, TaskAdd, TaskId, TaskIdError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/add")
async def add_task(task: Annotated[TaskAdd, Depends()]) -> TaskId:
    task_id = await TaskRepository.add_one(task)
    return {"status": "ok", "task_id": task_id}

@router.get("/read")
async def read_tasks() -> list[Task]:
    tasks = await TaskRepository.read_all()
    return tasks

@router.post("/change")
async def change_task(task: Annotated[Task, Depends()]) -> TaskId | TaskIdError:
    server_message = await TaskRepository.update_one(task)
    return server_message