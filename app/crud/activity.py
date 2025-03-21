from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.activity import Activity


async def create_activity(db: AsyncSession, name: str, parent_id: Optional[int] = None) -> Activity:
    new_activity = Activity(name=name, parent_id=parent_id)
    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)
    return new_activity


async def get_activity_by_id(db: AsyncSession, activity_id: int) -> Activity | None:
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    return result.scalar_one_or_none()


async def get_all_activities(db: AsyncSession) -> list[Activity]:
    result = await db.execute(select(Activity))
    return result.scalars().all()
