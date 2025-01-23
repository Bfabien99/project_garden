import uuid
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date


# Enum pour les statuts des projets
class ProjectStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PENDING = "pending"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


# Modèle principal pour les organisations
class Organization(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True, unique=True)
    name: str = Field(..., max_length=100, index=True, unique=True)
    short_name: Optional[str] = Field(default=None, max_length=100)
    logo: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=300)

    # Relation avec les projets
    projects: List["Project"] = Relationship(back_populates="organization")


# Modèle principal pour les projets
class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True, unique=True)
    logo: Optional[str] = Field(default=None)
    title: str = Field(..., max_length=150)
    description: Optional[str] = Field(default=None)
    status: ProjectStatus = Field(default=ProjectStatus.IN_PROGRESS)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    organization_id: str = Field(foreign_key="organization.uuid")

    # Relation avec l'organisation
    organization: Organization = Relationship(back_populates="projects")


# Modèle pour la création d'une organisation
class CreateOrganization(SQLModel):
    logo: Optional[str] = Field(default=None)
    name: str = Field(..., max_length=100, index=True, unique=True)
    short_name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)


# Modèle pour la création d'un projet
class CreateProject(SQLModel):
    logo: Optional[str] = Field(default=None)
    title: str = Field(..., max_length=150)
    description: Optional[str] = Field(default=None)
    status: ProjectStatus = Field(default=ProjectStatus.IN_PROGRESS)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    organization_id: str


# Modèle pour récupérer un projet
class RetrieveProject(SQLModel):
    logo: str
    uuid: str
    title: str
    description: Optional[str]
    status: ProjectStatus
    start_date: Optional[date]
    end_date: Optional[date]
    organization_id: str

# Modèle pour récupérer une organisation avec ses projets
class RetrieveOrganisation(SQLModel):
    uuid: str
    name: str
    short_name: str
    logo: str
    description: Optional[str]
    projects: List[RetrieveProject] = Field(default_factory=list)


# Modèle pour la mise à jour d'une organisation
class UpdateOrganization(SQLModel):
    logo: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

class UpdateProject(SQLModel):
    logo: Optional[str]
    title: Optional[str]
    description: Optional[str]
    status: Optional[ProjectStatus]
    start_date: Optional[date]
    end_date: Optional[date]
    organization_id: Optional[str]