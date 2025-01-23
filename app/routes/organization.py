from fastapi import APIRouter
from sqlmodel import select
from dependencies import SessionDep
from models import CreateOrganization, Organization, RetrieveOrganisation
from typing import List

router = APIRouter(prefix="/organizations")

@router.get("")
async def get_all_organizations_with_pagination(session: SessionDep, skip: int = 0, limit: int = 20):
    return session.exec(select(Organization).offset(skip).limit(limit)).all()

@router.get("/all", response_model=List[RetrieveOrganisation])
async def get_all_organizations(session: SessionDep):
    return session.exec(select(Organization)).all()