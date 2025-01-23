from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from dependencies import SessionDep
from models import CreateOrganization, Organization, RetrieveOrganisation
from typing import List
import markupsafe

router = APIRouter(prefix="/organizations")

#### Utilities functions to go faster
def get_by_name(name: str, session: SessionDep):
    name = name.lower()
    return session.exec(select(Organization).where(Organization.name == name)).one_or_none()

def get_by_uuid(uuid: str, session: SessionDep):
    uuid = uuid.lower()
    return session.exec(select(Organization).where(Organization.uuid == uuid)).one_or_none()
########################

########################
############ API ROUTES
@router.get("")
async def get_all_organizations_with_pagination(session: SessionDep, skip: int = 0, limit: int = 20):
    return session.exec(select(Organization).offset(skip).limit(limit)).all()

@router.post("")
async def add_an_organization(organization: CreateOrganization, session: SessionDep):
    name = markupsafe.escape_silent(organization.name.lower())
    logo = markupsafe.escape_silent(organization.logo)
    short_name = markupsafe.escape_silent(organization.short_name.upper())
    if get_by_name(name, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization 'name' value already exist")
    
    save_org = Organization(name=name, description=organization.description, logo=logo, short_name=short_name)
    session.add(save_org)
    session.commit()
    session.refresh(save_org)
    return RetrieveOrganisation(uuid=save_org.uuid, name=save_org.name, description=save_org.description, logo=save_org.logo, short_name=save_org.short_name)

@router.get("/all", response_model=List[RetrieveOrganisation])
async def get_all_organizations(session: SessionDep):
    return session.exec(select(Organization)).all()

@router.get("/{uuid}", response_model=RetrieveOrganisation)
async def get_an_organization(session: SessionDep, uuid: str):
    if not get_by_uuid(uuid, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization #{uuid} not found")
    return get_by_uuid(uuid, session)

@router.delete("/{uuid}")
async def delete_an_organization(session: SessionDep, uuid: str):
    if not get_by_uuid(uuid, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization #{uuid} not found")
    organization = get_by_uuid(uuid, session)
    session.delete(organization)
    session.commit()
    return {"detail": f"Organization #{uuid} deleted"}