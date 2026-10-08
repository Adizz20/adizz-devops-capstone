from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class BookingBase(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    destination: str = Field(min_length=2, max_length=100)
    travel_date: date
    number_of_people: int = Field(ge=1, le=20)
    status: str = Field(default="confirmed", max_length=30)


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    customer_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    destination: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    travel_date: date | None = None
    number_of_people: int | None = Field(
        default=None,
        ge=1,
        le=20,
    )
    status: str | None = Field(
        default=None,
        max_length=30,
    )


class BookingResponse(BookingBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)