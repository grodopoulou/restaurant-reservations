from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from reservations.infrastructure.orm import Base, ReservationRecord



def test_reservation_record_is_saved_and_read_back():
    """
    Test that a ReservationRecord saved in one session can be read back unchanged in a new session.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    reservation_id=uuid4()
    reservation = ReservationRecord(
        id=reservation_id, 
        surname="Παπαδοπούλου", 
        firstname="Μαρία", 
        email="papadopoulou@gmail.com", 
        phone="6979999999", 
        guest_count= 4, 
        arrival_slot= datetime(2026, 11, 14, 21, 0), 
        status="CONFIRMED"
        )

    with Session(engine) as session:
        session.add(reservation)
        session.commit()

    with Session(engine) as session:
        loaded = session.get(ReservationRecord, reservation_id)
        assert loaded.id == reservation_id
        assert loaded.surname == "Παπαδοπούλου"
        assert loaded.firstname == "Μαρία"
        assert loaded.email == "papadopoulou@gmail.com"
        assert loaded.phone == "6979999999"
        assert loaded.guest_count == 4
        assert loaded.arrival_slot == datetime(2026, 11, 14, 21, 0)
        assert loaded.status == "CONFIRMED"