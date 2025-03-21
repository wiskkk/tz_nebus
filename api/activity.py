from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.activity import (create_activity, get_activity_by_id,
                               get_all_activities)
from db.session import get_db
from schemas.activity import ActivityCreate, ActivityOut

router = APIRouter()


@router.post("/activities/", response_model=ActivityOut)
async def create_activity_view(activity: ActivityCreate, db: AsyncSession = Depends(get_db)):
    return await create_activity(db, activity.name, activity.parent_id)


@router.get("/activities/{activity_id}", response_model=ActivityOut)
async def read_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    return await get_activity_by_id(db, activity_id)


@router.get("/activities/", response_model=List[ActivityOut])
async def read_all_activities(db: AsyncSession = Depends(get_db)):
    return await get_all_activities(db)
