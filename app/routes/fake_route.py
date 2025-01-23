from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from dependencies import SessionDep
from models import (
    Organization,
    RetrieveOrganisation,
    Project,
    RetrieveProject,
    ProjectStatus,
)
from faker import Faker
import markupsafe

router = APIRouter(prefix="/api/fakers", tags=["faker"])
fake = Faker()
# localhost = "http://localhost:8000"


def get_by_title(title: str, session: SessionDep):
    title = markupsafe.escape_silent(title.lower())
    return session.exec(select(Project).where(Project.title == title)).one_or_none()


@router.post("/organizations")
async def create_fake_organization(session: SessionDep):
    # Générer les données fictives
    name = fake.company().lower()
    short_name = fake.company_suffix().upper()
    description = fake.text(max_nb_chars=300)
    logo = fake.image_url()

    organization = Organization(
        name=name, logo=logo, short_name=short_name, description=description
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


@router.post("/organizations/{uuid}/project")
async def create_fake_organization(session: SessionDep, uuid: str):
    organization = session.exec(
        select(Organization).where(Organization.uuid == uuid)
    ).one_or_none()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation #{uuid} not found",
        )

    # Générer les données fictives
    title = fake.text(50)
    end_date = fake.date_between()
    start_date = fake.date_between()
    description = fake.text(max_nb_chars=300)
    logo = fake.image_url()
    status = ProjectStatus.IN_PROGRESS

    if get_by_title(title, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project 'title' value already exist",
        )

    project = Project(
        title=title,
        description=description,
        logo=logo,
        start_date=start_date,
        end_date=end_date,
        organization_id=organization.uuid,
        status=status,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return RetrieveProject(
        uuid=project.uuid,
        title=project.title,
        description=project.description,
        logo=project.logo,
        start_date=project.start_date,
        end_date=project.end_date,
        organization_id=organization.uuid,
        status=project.status,
    )
