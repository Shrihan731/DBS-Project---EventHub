from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Service
from ..schemas import ServiceCreate, ServiceResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    existing = db.scalar(
        select(Service).where(Service.service_name == service.service_name)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Service already exists")

    new_service = Service(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.scalars(select(Service)).all()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
