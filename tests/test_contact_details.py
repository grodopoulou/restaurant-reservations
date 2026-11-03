import pytest
from reservations.domain.contact_details import ContactDetails

def test_valid_contact_details():
    contact = ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999")
    assert contact.surname == "Παπαδοπούλου"
    assert contact.firstname == "Μαρία"
    assert contact.email == "papadopoulou@example.com"
    assert contact.phone == "6979999999"


def test_zero_surname():
    with pytest.raises(ValueError):
        ContactDetails("", "Μαρία", "papadopoulou@example.com", "6979999999")


def test_zero_firstname():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "", "papadopoulou@example.com", "6979999999")


def test_email():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou.example.com", "6979999999")


def test_zero_email():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "", "6979999999")


def test_zero_phone():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "")


def test_phone_is_digit():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "69abs99999")


def test_phone_len():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "69799999999")


def test_phone_len():
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "697999999")