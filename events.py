from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Event, Organization, User
from ..schemas import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    organizer = db.get(User, event.organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer/user not found")

    organization = db.get(Organization, event.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    new_event = Event(**event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.scalars(select(Event).order_by(Event.event_date)).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)
    db.commit()

    return None
