from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.models.activity import Activity
from db.models.organization import Organization
from schemas.organization import OrganizationCreate, OrganizationOut


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


# async def create_organization(
#     db: AsyncSession, name: str, inn: str, phones: str, building_id: int, activity_ids: List[int]
# ) -> Organization:
#     organization = Organization(
#         name=name, inn=inn, phones=phones, building_id=building_id)
#     db.add(organization)
#     await db.commit()
#     await db.refresh(organization)

#     # Добавить активности
#     for activity_id in activity_ids:
#         activity = await db.get(Activity, activity_id)
#         if activity:
#             organization.activities.append(activity)

#     await db.commit()
#     await db.refresh(organization)
#     return organization


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

    :param db: Асинхронная сессия SQLAlchemy.
    :param inn: ИНН организации.
    :param name: Название организации.
    :param phones: Телефоны организации.
    :param building_id: ID здания.
    :param activity_ids: Список ID видов деятельности.
    :return: Сериализованные данные созданной организации.
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

    organization.activities.extend(activities)

    await db.commit()
    await db.refresh(organization, attribute_names=["activities"])

    return OrganizationOut.model_validate(organization)

