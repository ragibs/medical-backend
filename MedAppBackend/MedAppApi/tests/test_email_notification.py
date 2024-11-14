import pytest
from django.contrib.auth.models import User
from django.core import mail
from MedAppApi.models import UserProfile
from MedAppApi.views import send_email

@pytest.mark.django_db
def test_send_email():
    # Create a user with email and first name
    user = User.objects.create_user(username="testuser", email="test@example.com", first_name="Test", password="password")

    # Create user profile if necessary
    UserProfile.objects.create(user=user, role="patient")

    # Call send_email function
    send_email(user)

    # Check that one message has been sent
    assert len(mail.outbox) == 1, f"Expected 1 email, but {len(mail.outbox)} were sent."

    email = mail.outbox[0]
    
    # Assert email properties
    assert email.subject == "Welcome to Medical!", f"Expected subject 'Welcome to Medical!', got '{email.subject}'"
    assert "Test" in email.body, "Email body does not contain the user's first name."
    assert email.to == [user.email], f"Expected email recipient {user.email}, got {email.to}"
