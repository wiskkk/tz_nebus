from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.activity import Activity
from db.models.building import Building
from db.models.organization import Organization


async def search_organizations(
    db: AsyncSession,
    name: Optional[str] = None,
    building_address: Optional[str] = None,
    activity_name: Optional[str] = None,
) -> List[Organization]:
    """
    Поиск организаций по названию, адресу здания и имени активности.
    Все фильтры необязательны и могут комбинироваться.
    """
    stmt = select(Organization).options(
        joinedload(Organization.building),
        joinedload(Organization.activities)
    )

    if name:
        stmt = stmt.where(Organization.name.ilike(f"%{name}%"))
    if building_address:
        stmt = stmt.join(Organization.building).where(
            Building.address.ilike(f"%{building_address}%"))
    if activity_name:
        stmt = stmt.join(Organization.activities).where(
            Activity.name.ilike(f"%{activity_name}%"))

    result = await db.execute(stmt)
    return result.scalars().unique().all()
