import asyncio

from sqlalchemy.exc import IntegrityError

from db.models.activity import Activity
from db.models.building import Building
from db.models.organization import Organization
from db.session import AsyncSessionLocal


async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # Создание зданий с координатами
            building1 = Building(
                address="Улица Пушкина, 1",
                latitude=55.7558,
                longitude=37.6176
            )
            building2 = Building(
                address="Улица Лермонтова, 2",
                latitude=55.7600,
                longitude=37.6200
            )

            # Создание активностей
            activity1 = Activity(name="Спорт")
            activity2 = Activity(name="Образование")
            activity3 = Activity(name="Искусство")

            session.add_all(
                [building1, building2, activity1, activity2, activity3])
            await session.commit()

            await session.refresh(building1)
            await session.refresh(building2)
            await session.refresh(activity1)
            await session.refresh(activity2)
            await session.refresh(activity3)

            # Создание организаций с телефонами и связями с активностями
            org1 = Organization(
                name="Фитнес Центр",
                phones="123-456-7890",
                building_id=building1.id
            )
            org1.activities.extend([activity1])

            org2 = Organization(
                name="Школа №1",
                phones="987-654-3210",
                building_id=building1.id
            )
            org2.activities.extend([activity2])

            org3 = Organization(
                name="Галерея Искусств",
                phones="555-555-5555",
                building_id=building2.id
            )
            org3.activities.extend([activity3, activity2])

            session.add_all([org1, org2, org3])
            await session.commit()

            print("✅ Данные успешно добавлены!")

        except IntegrityError as e:
            print(f"❌ Ошибка при добавлении данных: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(seed_data())
