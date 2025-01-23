from fastapi import APIRouter, HTTPException, status
from dependencies import SessionDep
from models import Organization, RetrieveOrganisation
from faker import Faker

router = APIRouter(prefix="/fakers")
fake = Faker()
localhost = "http://localhost:8000"


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
