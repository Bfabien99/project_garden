from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func
from dependencies import SessionDep
from models import CreateProject, Project, RetrieveProject, UpdateProject, Organization
import markupsafe
import math

router = APIRouter(prefix="/api/projects", tags=["projects"])


#### Utilities functions to go faster
def get_by_title(title: str, session: SessionDep):
    title = markupsafe.escape_silent(title.lower())
    return session.exec(select(Project).where(Project.title == title)).one_or_none()


def get_by_uuid(uuid: str, session: SessionDep):
    uuid = uuid.lower()
    return session.exec(select(Project).where(Project.uuid == uuid)).one_or_none()


########################


########################
############ API ROUTES
@router.get("")
async def get_all_projects_with_pagination(
    session: SessionDep, skip: int = 0, limit: int = 20
):
    total = session.exec(select(func.count(Project.id))).one()
    page = math.ceil(total / limit)
    projects = session.exec(select(Project).offset(skip).limit(limit)).all()
    return {"total": total, "pages": page, "data": projects}


@router.post("")
async def add_an_project(project: CreateProject, session: SessionDep):
    title = markupsafe.escape_silent(project.title.lower())
    logo = markupsafe.escape_silent(project.logo)
    description = markupsafe.escape_silent(project.description)
    if get_by_title(title, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project 'title' value already exist",
        )

    organization = session.exec(
        select(Organization).where(Organization.uuid == project.organization_id)
    ).one_or_none()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organisation #{project.organization_id} not found",
        )

    save_pro = Project(
        title=title,
        description=description,
        logo=logo,
        start_date=project.start_date,
        end_date=project.end_date,
        organization_id=project.organization_id,
        status=project.status,
    )
    session.add(save_pro)
    session.commit()
    session.refresh(save_pro)
    return RetrieveProject(
        uuid=save_pro.uuid,
        title=save_pro.title,
        description=save_pro.description,
        logo=save_pro.logo,
        start_date=save_pro.start_date,
        end_date=save_pro.end_date,
        organization_id=organization.uuid,
        status=save_pro.status,
    )


@router.get("/all")
async def get_all_projects(session: SessionDep):
    total = session.exec(select(func.count(Project.id))).one()
    projects = session.exec(select(Project)).all()
    return {"total": total, "data": projects}


@router.get("/{uuid}")
async def get_a_project(session: SessionDep, uuid: str):
    project = get_by_uuid(uuid, session)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project #{uuid} not found",
        )
    org = session.exec(
        select(Organization).where(Organization.uuid == project.organization_id)
    ).one_or_none()
    return {"project": project, "organization": org}


@router.put("/{uuid}", response_model=RetrieveProject)
async def update_a_project(session: SessionDep, uuid: str, update_pro: UpdateProject):
    project = get_by_uuid(uuid, session)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project #{uuid} not found",
        )

    if update_pro.title:
        is_title = get_by_title(update_pro.title, session)
        if is_title and is_title.uuid != project.uuid:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project 'title' value already exist",
            )
        project.title = markupsafe.escape_silent(update_pro.title.lower())

    if update_pro.logo:
        project.logo = markupsafe.escape_silent(update_pro.logo)

    if update_pro.description:
        project.description = markupsafe.escape_silent(update_pro.description)

    if update_pro.status:
        project.status = update_pro.status

    if update_pro.start_date:
        project.start_date = update_pro.start_date

    if update_pro.end_date:
        project.end_date = update_pro.end_date

    if update_pro.organization_id:
        organization = session.exec(
            select(Organization).where(Organization.uuid == update_pro.organization_id)
        ).one_or_none()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organisation #{project.organization_id} not found",
            )
        project.organization_id = update_pro.organization_id

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
        organization_id=project.organization_id,
        status=project.status,
    )


@router.delete("/{uuid}")
async def delete_a_project(session: SessionDep, uuid: str):
    project = get_by_uuid(uuid, session)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project #{uuid} not found",
        )
    session.delete(project)
    session.commit()
    return {"detail": f"Project #{uuid} deleted"}
