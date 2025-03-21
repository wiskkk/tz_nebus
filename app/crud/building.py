from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.building import Building


async def create_building(db: AsyncSession, address: str, latitude: float, longitude: float) -> Building:
    new_building = Building(
        address=address, latitude=latitude, longitude=longitude)
    db.add(new_building)
    await db.commit()
    await db.refresh(new_building)
    return new_building


async def get_building_by_id(db: AsyncSession, building_id: int) -> Building | None:
    result = await db.execute(select(Building).where(Building.id == building_id))
    return result.scalar_one_or_none()


async def get_all_buildings(db: AsyncSession) -> list[Building]:
    result = await db.execute(select(Building))
    return result.scalars().all()
