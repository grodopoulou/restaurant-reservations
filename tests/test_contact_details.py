import pytest
from reservations.domain.contact_details import ContactDetails

def test_valid_contact_details():
    contact = ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999")
    assert contact.surname == "Παπαδοπούλου"
    assert contact.firstname == "Μαρία"
    assert contact.email == "papadopoulou@example.com"
    assert contact.phone == "6979999999"


def test_zero_surname():
    """Test that will be raised a ValueError if there is no surname given."""
    with pytest.raises(ValueError):
        ContactDetails("", "Μαρία", "papadopoulou@example.com", "6979999999")


def test_zero_firstname():
    """Test that will be raised a ValueError if there is no firstname given."""
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "", "papadopoulou@example.com", "6979999999")


def test_email():
    """
    Test that will be raised a ValueError if the email is not valid. Given that a valid email has the character: @
    """
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou.example.com", "6979999999")


def test_zero_email():
    """Test that will be raised a ValueError if there is no email given."""
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "", "6979999999")


def test_zero_phone():
    """Test that will be raised a ValueError if there is no phone number given."""
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "")


def test_phone_is_digit():
    """
    Test that will be raised a ValueError if the phone number does not consist of digits.
    """
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "69abs99999")


def test_phone_len():
    """
    Test that will be raised a ValueError if the phone number has more than ten digits.
    """
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "69799999999")


def test_phone_len():
    """
    Test that will be raised a ValueError if the phone number has less than ten digits.
    """
    with pytest.raises(ValueError):
        ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "697999999")