from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.activity import Activity
from schemas.activity import ActivityOut


async def create_activity(
    db: AsyncSession, name: str, parent_id: Optional[int] = None
) -> ActivityOut:
    """
    Создание активности с проверкой на максимальную вложенность (3 уровня).
    """
    if parent_id is not None:
        depth = await get_activity_depth(db, parent_id)
        if depth >= 3:
            raise HTTPException(
                status_code=400,
                detail="Превышен допустимый уровень вложенности (максимум 3 уровня)"
            )

    activity = Activity(name=name, parent_id=parent_id)
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return ActivityOut.model_validate(activity)


async def get_activity_by_id(db: AsyncSession, activity_id: int) -> Activity | None:
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    return result.scalar_one_or_none()


async def get_all_activities(db: AsyncSession) -> list[Activity]:
    result = await db.execute(select(Activity))
    return result.scalars().all()


async def get_activity_with_descendants(
    db: AsyncSession, root_name: str
) -> List[Activity]:
    """
    Получает активность по имени и её потомков до 3 уровня вложенности.
    """
    # Находим корневую активность по имени
    result = await db.execute(select(Activity).where(Activity.name == root_name))
    root_activity = result.scalar_one_or_none()
    if not root_activity:
        return []

    # Собираем ID всех потомков вручную (до 3 уровней)
    ids_to_check = [root_activity.id]
    all_activities = [root_activity]

    result = await db.execute(select(Activity).where(Activity.parent_id == root_activity.id))
    level1 = result.scalars().all()
    all_activities.extend(level1)
    ids_to_check.extend([act.id for act in level1])

    if level1:
        result = await db.execute(select(Activity).where(Activity.parent_id.in_([a.id for a in level1])))
        level2 = result.scalars().all()
        all_activities.extend(level2)
        ids_to_check.extend([act.id for act in level2])

    if level2:
        result = await db.execute(select(Activity).where(Activity.parent_id.in_([a.id for a in level2])))
        level3 = result.scalars().all()
        all_activities.extend(level3)
        ids_to_check.extend([act.id for act in level3])

    return all_activities


async def get_activity_depth(db: AsyncSession, activity_id: int) -> int:
    """
    Рекурсивно вычисляет глубину активности по parent_id.
    Максимум возвращает 3.
    """
    depth = 1
    current_id = activity_id

    while True:
        result = await db.execute(select(Activity).where(Activity.id == current_id))
        activity = result.scalar_one_or_none()
        if activity is None or activity.parent_id is None:
            break
        depth += 1
        if depth > 3:
            break
        current_id = activity.parent_id

    return depth
