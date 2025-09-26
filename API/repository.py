from database import new_session, TaskOrm
from schemas import Task, TaskAdd, TaskId, TaskIdError
from sqlalchemy import select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def read_all(cls) -> list[Task]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [Task.model_validate(task) for task in task_models]
            return task_schemas

    @classmethod
    async def update_one(cls, data: Task) -> TaskId | TaskIdError:
        async with new_session() as session:
            task_dict = data.model_dump()
            query = select(TaskOrm).where(TaskOrm.id == task_dict["id"])
            result = await session.execute(query)
            task: TaskOrm | None = result.scalar_one_or_none()

            if task is None:
                return {"status": "error", "message": "bad index entered"}

            for field, value in task_dict.items():
                setattr(task, field, value)

            await session.commit()
            await session.refresh(task)

            return {"status": "ok", "task_id": task_dict["id"]}