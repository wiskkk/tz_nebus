from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.building import (create_building, get_all_buildings,
                               get_building_by_id)
from db.session import get_db
from schemas.building import BuildingCreate, BuildingOut

router = APIRouter()


@router.post("/buildings/", response_model=BuildingOut)
async def create_building_view(building: BuildingCreate, db: AsyncSession = Depends(get_db)):
    return await create_building(db, building.address, building.latitude, building.longitude)


@router.get("/buildings/{building_id}", response_model=BuildingOut)
async def read_building(building_id: int, db: AsyncSession = Depends(get_db)):
    return await get_building_by_id(db, building_id)


@router.get("/buildings/", response_model=List[BuildingOut])
async def read_all_buildings(db: AsyncSession = Depends(get_db)):
    return await get_all_buildings(db)
