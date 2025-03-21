from typing import List

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    inn: str
    phones: str
    building_id: int
    activity_ids: List[int]


class OrganizationOut(BaseModel):
    id: int
    name: str
    inn: str
    phones: str
    building_id: int
    activity_ids: List[int]

    model_config = {
        "from_attributes": True
    }
