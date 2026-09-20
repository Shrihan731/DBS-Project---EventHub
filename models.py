from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# M:N relationship between Vendor and Service.
vendor_service = Table(
    "vendor_service",
    Base.metadata,
    Column("vendor_id", ForeignKey("vendors.id", ondelete="CASCADE"), primary_key=True),
    Column("service_id", ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(String(30), default="organizer", nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="organizer")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    organization_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(150), nullable=True)

    events: Mapped[list["Event"]] = relationship(back_populates="organization")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_name: Mapped[str] = mapped_column(String(150), nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    venue: Mapped[str] = mapped_column(String(200), nullable=False)
    expected_attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    organizer: Mapped["User"] = relationship(back_populates="events")
    organization: Mapped["Organization"] = relationship(back_populates="events")
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vendor_name: Mapped[str] = mapped_column(String(150), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)

    services: Mapped[list["Service"]] = relationship(
        secondary=vendor_service,
        back_populates="vendors",
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="vendor")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    vendors: Mapped[list["Vendor"]] = relationship(
        secondary=vendor_service,
        back_populates="services",
    )
    bookings: Mapped[list["Booking"]] = relationship(back_populates="service")


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "vendor_id",
            "service_id",
            name="uq_event_vendor_service",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)

    booking_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="booked", nullable=False)

    event: Mapped["Event"] = relationship(back_populates="bookings")
    vendor: Mapped["Vendor"] = relationship(back_populates="bookings")
    service: Mapped["Service"] = relationship(back_populates="bookings")
    review: Mapped["Review | None"] = relationship(
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Review(Base):
    # Model included now so the database design is ready for Review 2.
    # API endpoints are intentionally NOT implemented in this 50% version.
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("booking_id", name="uq_review_booking"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    quality_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reliability_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    value_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    booking: Mapped["Booking"] = relationship(back_populates="review")
    user: Mapped["User"] = relationship(back_populates="reviews")
