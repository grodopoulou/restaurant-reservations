from sqlalchemy import String, Integer, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from uuid import UUID


class Base(DeclarativeBase):
    """Declarative base class from which all ORM models inherit."""
    pass


class ReservationRecord(Base):
    """
    A single guest reservation (table "reservations").

    Attributes:
        id (UUID): Unique identifier of the reservation (primary key).
        surname (str): Guest's last name, up to 50 characters.
        firstname (str): Guest's first name, up to 50 characters.
        email (str): Guest's contact email, up to 100 characters.
        phone (str): Guest's contact phone number, up to 10 characters.
        guest_count (int): Number of guests included in the reservation.
        arrival_slot (datetime): Date and time slot of the guest's arrival.
        status (str): Current state of the reservation ("confirmed" or "cancelled").
    """
    __tablename__ = "reservations"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )

    surname: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    firstname: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    phone: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    guest_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    arrival_slot: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )