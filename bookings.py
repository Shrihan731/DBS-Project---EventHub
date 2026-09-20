from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Booking, Event, Service, Vendor
from ..schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    event = db.get(Event, booking.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    vendor = db.get(Vendor, booking.vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    service = db.get(Service, booking.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service not in vendor.services:
        raise HTTPException(
            status_code=400,
            detail="This vendor is not registered for the selected service",
        )

    existing = db.scalar(
        select(Booking).where(
            Booking.event_id == booking.event_id,
            Booking.vendor_id == booking.vendor_id,
            Booking.service_id == booking.service_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A booking already exists for this event/vendor/service combination",
        )

    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.get("/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.scalars(select(Booking)).all()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
