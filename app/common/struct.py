
from typing import Optional
from pydantic import BaseModel

class TaskStruct(BaseModel):
    id: Optional[int]
    name: str
    status: int

    class Config:
        orm_mode = True
