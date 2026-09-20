from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Organization
from ..schemas import OrganizationCreate, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(Organization).where(Organization.name == organization.name)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    new_org = Organization(**organization.model_dump())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org


@router.get("/", response_model=list[OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    return db.scalars(select(Organization)).all()


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = db.get(Organization, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization
