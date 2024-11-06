import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from MedAppApi.serializers import (
    UserRegistrationSerializer, 
    DoctorRegistrationSerializer, 
    PatientRegistrationSerializer, 
    AuthPatientRegistrationSerializer, 
    AdminStaffRegistrationSerializer
)
from MedAppApi.models import Doctor, Patient, AdminStaff, PatientDetails, Availability, Testimonials, Ratings

@pytest.mark.django_db
def test_user_registration_serializer():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "username": "john_doe",
        "password": "password123"
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.first_name == "John"
    assert user.email == "john@example.com"
    assert user.check_password("password123")


@pytest.mark.django_db
def test_doctor_registration_serializer():
    user_data = {
        "first_name": "Dr. Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "username": "jane_doe",
        "password": "password123"
    }
    doctor_data = {
        "user": user_data,
        "specialization": "Cardiology"
    }
    serializer = DoctorRegistrationSerializer(data=doctor_data)
    assert serializer.is_valid()
    doctor = serializer.save()
    assert doctor.user.first_name == "Dr. Jane"
    assert doctor.specialization == "Cardiology"


@pytest.mark.django_db
def test_patient_registration_serializer():
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "username": "alice_smith",
        "password": "password123"
    }
    patient_data = {
        "user": user_data,
        "phone": "123-456-7890",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zipcode": "90210"
    }
    serializer = PatientRegistrationSerializer(data=patient_data)
    assert serializer.is_valid()
    patient = serializer.save()
    assert patient.user.first_name == "Alice"
    assert patient.phone == "123-456-7890"


@pytest.mark.django_db
def test_auth_patient_registration_serializer():
    data = {
        "username": "charlie_brown",
        "email": "charlie@example.com",
        "password1": "password123",
        "password2": "password123",
        "first_name": "Charlie",
        "last_name": "Brown",
        "phone": "987-654-3210",
        "address": "456 Elm St",
        "city": "Hometown",
        "state": "NY",
        "zipcode": "10001"
    }
    serializer = AuthPatientRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save(request=None)
    assert user.first_name == "Charlie"
    assert Patient.objects.filter(user=user).exists()
    assert Patient.objects.get(user=user).phone == "987-654-3210"


@pytest.mark.django_db
def test_admin_staff_registration_serializer():
    user_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "username": "admin_user",
        "password": "admin123"
    }
    admin_data = {
        "user": user_data,
        "position": "Support"
    }
    serializer = AdminStaffRegistrationSerializer(data=admin_data)
    assert serializer.is_valid()
    admin_staff = serializer.save()
    assert admin_staff.user.first_name == "Admin"
    assert admin_staff.position == "Support"


@pytest.mark.django_db
def test_invalid_user_registration_serializer():
    # Test with missing required fields
    data = {
        "first_name": "Incomplete",
        "email": "incomplete@example.com"
        # Missing 'username' and 'password'
    }
    serializer = UserRegistrationSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_patient_details_serializer():
    patient = Patient.objects.create(
        user=User.objects.create_user(username="test_patient", password="password123"),
        phone="111-222-3333",
        address="789 Maple St",
        city="Big City",
        state="TX",
        zipcode="75001"
    )
    serializer = PatientDetailsSerializer(patient)
    assert serializer.data["phone"] == "111-222-3333"


@pytest.mark.django_db
def test_availability_serializer():
    availability = Availability.objects.create(
        day="Monday",
        start_time="09:00",
        end_time="17:00"
    )
    serializer = AvailabilitySerializer(availability)
    assert serializer.data["day"] == "Monday"


@pytest.mark.django_db
def test_testimonials_serializer():
    testimonial = Testimonials.objects.create(
        user=User.objects.create_user(username="user_testimonial", password="password123"),
        message="Great service!"
    )
    serializer = TestimonialsSerializer(testimonial)
    assert serializer.data["message"] == "Great service!"


@pytest.mark.django_db
def test_ratings_serializer():
    rating = Ratings.objects.create(
        user=User.objects.create_user(username="user_rating", password="password123"),
        rating=5
    )
    serializer = RatingsSerializer(rating)
    assert serializer.data["rating"] == 5
