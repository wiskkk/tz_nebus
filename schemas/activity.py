from typing import Optional

from pydantic import BaseModel


class ActivityCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True
