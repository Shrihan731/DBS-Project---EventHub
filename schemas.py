from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=10)
    role: str = Field(default="organizer", max_length=30)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class OrganizationBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    organization_type: str | None = Field(default=None, max_length=50)
    contact_email: EmailStr | None = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EventBase(BaseModel):
    event_name: str = Field(min_length=2, max_length=150)
    event_type: str = Field(min_length=2, max_length=80)
    event_date: datetime
    venue: str = Field(min_length=2, max_length=200)
    expected_attendees: int = Field(ge=1)
    description: str | None = None
    organizer_id: int
    organization_id: int


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class VendorBase(BaseModel):
    vendor_name: str = Field(min_length=2, max_length=150)
    company_name: str | None = Field(default=None, max_length=150)
    contact_number: str = Field(min_length=10, max_length=10)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=250)


class VendorCreate(VendorBase):
    pass


class VendorResponse(VendorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ServiceBase(BaseModel):
    service_name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=80)
    description: str | None = None


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class VendorServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    vendor_id: int
    service_id: int


class BookingBase(BaseModel):
    event_id: int
    vendor_id: int
    service_id: int
    amount: float = Field(ge=0)
    status: str = Field(default="booked", max_length=30)


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    booking_date: datetime


# Prepared for the next review; no Review API is exposed yet.
class ReviewBase(BaseModel):
    booking_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    quality_rating: int | None = Field(default=None, ge=1, le=5)
    reliability_rating: int | None = Field(default=None, ge=1, le=5)
    value_rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)


class ReviewResponse(ReviewBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    review_date: datetime
