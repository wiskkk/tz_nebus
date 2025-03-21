from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.organization import (create_organization, get_organization_by_id,
                                   get_organizations_by_activity,
                                   get_organizations_by_building)
from app.crud.organization_crud import search_organizations
from db.session import get_db
from schemas.organization import OrganizationCreate, OrganizationOut

router = APIRouter()


@router.get("/organizations/search", response_model=List[OrganizationOut])
async def search_organizations_view(
    name: Optional[str] = Query(None),
    building_address: Optional[str] = Query(None),
    activity_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Фильтрация организаций по названию, адресу здания и активности.
    """
    return await search_organizations(db, name, building_address, activity_name)


@router.post("/organizations/", response_model=OrganizationOut)
async def create_organization_view(
    organization: OrganizationCreate, db: AsyncSession = Depends(get_db)
):
    org = await create_organization(
        db=db,
        inn=organization.inn,
        name=organization.name,
        phones=organization.phones,
        building_id=organization.building_id,
        activity_ids=organization.activity_ids
    )
    return org


@router.get("/organizations/{org_id}", response_model=OrganizationOut)
async def read_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    return await get_organization_by_id(db, org_id)


@router.get("/organizations/by_building/{building_id}", response_model=List[OrganizationOut])
async def read_organizations_by_building(
    building_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_organizations_by_building(db, building_id)


@router.get("/organizations/by_activity/{activity_name}", response_model=List[OrganizationOut])
async def read_organizations_by_activity(
    activity_name: str, db: AsyncSession = Depends(get_db)
):
    return await get_organizations_by_activity(db, activity_name)
