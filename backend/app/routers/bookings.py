from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking
from app.schemas import BookingCreate, BookingResponse, BookingUpdate


router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"],
)


@router.get(
    "",
    response_model=list[BookingResponse],
)
def get_bookings(
    db: Session = Depends(get_db),
):
    statement = select(Booking).order_by(Booking.id.desc())
    return db.scalars(statement).all()


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return booking


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
):
    booking = Booking(**booking_data.model_dump())

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    updates = booking_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)

    return booking


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    db.delete(booking)
    db.commit()