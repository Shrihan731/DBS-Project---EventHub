from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Service, Vendor
from ..schemas import VendorCreate, VendorResponse, VendorServiceResponse

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = Vendor(**vendor.model_dump())
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor


@router.get("/", response_model=list[VendorResponse])
def get_vendors(db: Session = Depends(get_db)):
    return db.scalars(select(Vendor)).all()


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.post(
    "/{vendor_id}/services/{service_id}",
    response_model=VendorServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_service_to_vendor(
    vendor_id: int,
    service_id: int,
    db: Session = Depends(get_db),
):
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service in vendor.services:
        raise HTTPException(status_code=400, detail="Service already assigned to vendor")

    vendor.services.append(service)
    db.commit()

    return {"vendor_id": vendor_id, "service_id": service_id}


# vendor can stop offering a particular service, but dont delete vendors info altogether as we want to preserve historical data for bookings
@router.delete(
    "/{vendor_id}/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_service_from_vendor(
    vendor_id: int,
    service_id: int,
    db: Session = Depends(get_db)
):
    vendor = db.get(Vendor, vendor_id)

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    service = db.get(Service, service_id)

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    if service not in vendor.services:
        raise HTTPException(
            status_code=404,
            detail="This service is not assigned to the vendor"
        )

    vendor.services.remove(service)
    db.commit()

    return None
