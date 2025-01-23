from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func
from dependencies import SessionDep
from models import (
    CreateOrganization,
    Organization,
    RetrieveOrganisation,
    UpdateOrganization,
)
import markupsafe
import math

router = APIRouter(prefix="/api/organizations", tags=["organizations"])


#### Utilities functions to go faster
def get_by_name(name: str, session: SessionDep):
    name = markupsafe.escape_silent(name.lower())
    return session.exec(
        select(Organization).where(Organization.name == name)
    ).one_or_none()


def get_by_uuid(uuid: str, session: SessionDep):
    uuid = uuid.lower()
    return session.exec(
        select(Organization).where(Organization.uuid == uuid)
    ).one_or_none()


########################


########################
############ API ROUTES
@router.get("")
async def get_all_organizations_with_pagination(
    session: SessionDep, skip: int = 0, limit: int = 20
):
    total = session.exec(select(func.count(Organization.id))).one()
    page = math.ceil(total / limit)
    organizations = session.exec(select(Organization).offset(skip).limit(limit)).all()
    return {"total": total, "pages": page, "data": organizations}


@router.post("")
async def add_an_organization(organization: CreateOrganization, session: SessionDep):
    name = markupsafe.escape_silent(organization.name.lower())
    logo = markupsafe.escape_silent(organization.logo)
    short_name = markupsafe.escape_silent(organization.short_name.upper())
    description = markupsafe.escape_silent(organization.description)
    if get_by_name(name, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization 'name' value already exist",
        )

    save_org = Organization(
        name=name, description=description, logo=logo, short_name=short_name
    )
    session.add(save_org)
    session.commit()
    session.refresh(save_org)
    return RetrieveOrganisation(
        uuid=save_org.uuid,
        name=save_org.name,
        description=save_org.description,
        logo=save_org.logo,
        short_name=save_org.short_name,
    )


@router.get("/all")
async def get_all_organizations(session: SessionDep):
    total = session.exec(select(func.count(Organization.id))).one()
    organizations = session.exec(select(Organization)).all()
    return {"total": total, "data": organizations}


@router.get("/{uuid}", response_model=RetrieveOrganisation)
async def get_an_organization(session: SessionDep, uuid: str):
    organization = get_by_uuid(uuid, session)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization #{uuid} not found",
        )
    return organization


@router.put("/{uuid}", response_model=RetrieveOrganisation)
async def update_an_organization(
    session: SessionDep, uuid: str, update_org: UpdateOrganization
):
    organization = get_by_uuid(uuid, session)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization #{uuid} not found",
        )

    if update_org.name:
        is_name = get_by_name(update_org.name, session)
        if is_name and is_name.uuid != organization.uuid:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization 'name' value already exist",
            )
        organization.name = markupsafe.escape_silent(update_org.name.lower())

    if update_org.description:
        organization.description = markupsafe.escape_silent(update_org.description)

    if update_org.logo:
        organization.logo = markupsafe.escape_silent(update_org.logo)

    if update_org.short_name:
        organization.short_name = markupsafe.escape_silent(
            update_org.short_name.upper()
        )

    session.add(organization)
    session.commit()
    session.refresh(organization)
    return RetrieveOrganisation(
        uuid=organization.uuid,
        name=organization.name,
        description=organization.description,
        logo=organization.logo,
        short_name=organization.short_name,
    )


@router.delete("/{uuid}")
async def delete_an_organization(session: SessionDep, uuid: str):
    organization = get_by_uuid(uuid, session)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization #{uuid} not found",
        )
    session.delete(organization)
    session.commit()
    return {"detail": f"Organization #{uuid} deleted"}
