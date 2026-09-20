from fastapi import FastAPI

from .database import Base, engine
from .routers import bookings, events, organizations, services, users, vendors

# Import models before create_all so SQLAlchemy knows every table.
from . import models  # noqa: F401


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EventHub API",
    description=(
        "Campus Event Vendor Management System. "
        "Stores events, vendors, services and historical bookings "
        "so future organizers can compare vendors."
    ),
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(events.router)
app.include_router(vendors.router)
app.include_router(services.router)
app.include_router(bookings.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to EventHub API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
