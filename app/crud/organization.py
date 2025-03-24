from math import asin, cos, radians, sin, sqrt
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from app.crud.activity import get_activity_with_descendants
from db.models.activity import Activity
from db.models.organization import Organization
from schemas.organization import OrganizationOut

EARTH_RADIUS_KM = 6371.0  # Радиус Земли в км


async def get_organization_by_id(db: AsyncSession, org_id: int) -> Optional[Organization]:
    """Получить организацию по id."""
    query = select(Organization).filter(Organization.id == org_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_organizations_by_building(
    db: AsyncSession, building_id: int
) -> List[Organization]:
    """Получить список организаций по зданию."""
    query = (
        select(Organization)
        .filter(Organization.building_id == building_id)
        # Можно подгрузить связи
        .options(selectinload(Organization.activities))
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_organizations_by_activity(
    db: AsyncSession, activity_name: str
) -> List[Organization]:
    """Получить список организаций по виду деятельности."""
    query = (
        select(Organization)
        .join(Organization.activities)
        .filter(Activity.name == activity_name)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_organization(
    db: AsyncSession,
    inn: str,
    name: str,
    phones: str,
    building_id: int,
    activity_ids: List[int]
) -> OrganizationOut:
    """
    Создание новой организации и привязка к выбранным видам деятельности.
    """
    organization = Organization(
        inn=inn,
        name=name,
        phones=phones,
        building_id=building_id
    )
    db.add(organization)
    await db.flush()

    result = await db.execute(
        select(Activity).where(Activity.id.in_(activity_ids))
    )
    activities = result.scalars().all()

    if len(activities) != len(activity_ids):
        raise ValueError("One or more activity IDs do not exist.")

    if not all(isinstance(activity, Activity) for activity in activities):
        raise TypeError(
            "All elements in 'activities' must be instances of Activity.")

    await db.refresh(organization, attribute_names=["activities"])

    organization.activities.clear()
    organization.activities.extend(activities)

    await db.commit()
    await db.refresh(organization, attribute_names=["activities"])

    return OrganizationOut(
        id=organization.id,
        name=organization.name,
        inn=organization.inn,
        phones=organization.phones,
        building_id=organization.building_id,
        activity_ids=[activity.id for activity in organization.activities]
    )


def haversine(lat1, lon1, lat2, lon2):
    """Расчет расстояния между двумя точками (км)."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_KM * c


async def get_organizations_by_geo(
    db: AsyncSession,
    latitude: float,
    longitude: float,
    radius_km: Optional[float] = None,
    # (min_lat, max_lat, min_lon, max_lon)
    area: Optional[Tuple[float, float, float, float]] = None
) -> List[Organization]:
    query = select(Organization).options(joinedload(Organization.building))

    result = await db.execute(query)
    organizations = result.scalars().all()

    filtered = []
    for org in organizations:
        bld = org.building
        if bld is None:
            continue

        if radius_km:
            distance = haversine(latitude, longitude,
                                 bld.latitude, bld.longitude)
            if distance <= radius_km:
                filtered.append(org)
        elif area:
            min_lat, max_lat, min_lon, max_lon = area
            if min_lat <= bld.latitude <= max_lat and min_lon <= bld.longitude <= max_lon:
                filtered.append(org)

    return filtered


async def get_organizations_by_activity_tree(
    db: AsyncSession, root_activity_name: str
) -> List[Organization]:
    """
    Поиск организаций, связанных с видом деятельности и его потомками.
    """
    activities = await get_activity_with_descendants(db, root_activity_name)
    if not activities:
        return []

    activity_ids = [act.id for act in activities]

    result = await db.execute(
        select(Organization)
        .join(Organization.activities)
        .where(Activity.id.in_(activity_ids))
        .options(joinedload(Organization.activities), joinedload(Organization.building))
        .distinct()
    )
    organizations = result.scalars().all()
    return organizations
