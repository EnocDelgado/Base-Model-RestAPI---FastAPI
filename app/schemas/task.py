from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

# from pydantic.types import conint

class TaskBase(BaseModel):
    content: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# class TaskOut(BaseModel):
#     task: Task

#     class Config:
#         orm_mode = True