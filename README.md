# EventHub Backend — 50% Implementation

EventHub is a Campus Event Vendor Management System.

## Current scope (Review 1 / ~50%)
Implemented:
- FastAPI project structure
- SQLAlchemy database layer
- User, Organization, Event, Vendor, Service models
- Vendor-Service many-to-many relationship
- Event-Booking-Vendor-Service relationships
- Pydantic request/response schemas
- CRUD APIs for:
  - Users
  - Organizations
  - Events
  - Vendors
  - Services
  - Vendor-Service assignment
  - Bookings
- Basic validation and HTTP error handling
- SQLite by default so the project runs immediately
- Database URL can later be changed to Oracle/PostgreSQL

Intentionally left for the next phase:
- Authentication / JWT
- Role-based authorization
- Review APIs
- Vendor comparison/ranking
- Advanced search/filtering
- Dashboard/analytics
- File/image uploads
- Frontend
- Production deployment

## Project structure

eventhub_backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── users.py
│       ├── organizations.py
│       ├── events.py
│       ├── vendors.py
│       ├── services.py
│       └── bookings.py
├── .env.example
├── requirements.txt
└── README.md

## Setup on Windows

1. Open this folder in VS Code.

2. Create a virtual environment:
   python -m venv venv

3. Activate it:
   venv\Scripts\activate

4. Install packages:
   pip install -r requirements.txt

5. Run:
   uvicorn app.main:app --reload

6. Open:
   http://127.0.0.1:8000/docs

The Swagger UI lets you test all implemented APIs.

## Database

SQLite is used initially:
eventhub.db

This keeps the project easy to demonstrate. The database URL is controlled by the
DATABASE_URL environment variable.

Example:
DATABASE_URL=sqlite:///./eventhub.db

Later, you can switch to Oracle by changing the URL and installing an Oracle driver.
The model/repository structure is deliberately kept independent of SQLite.

## Suggested demo flow

1. Create an organization.
2. Create a user and use that user as organizer.
3. Create a vendor.
4. Create services such as Catering and Photography.
5. Assign services to the vendor.
6. Create an event under the organization.
7. Create a booking connecting Event + Vendor + Service.
8. Show the relationships through GET endpoints.

## Important design decision

A review is related to a BOOKING rather than directly to a VENDOR.

This means a future review can represent:
"Vendor X provided Catering for Event Y and received 4/5."

That allows EventHub to later calculate useful vendor history such as:
- average rating
- reliability
- average cost
- number of previous bookings
- event-specific performance

Those features are intentionally not implemented yet.
