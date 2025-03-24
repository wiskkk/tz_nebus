from pydantic import BaseModel


class BuildingCreate(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingOut(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = {
        "from_attributes": True
    }
