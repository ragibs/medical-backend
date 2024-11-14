import pytest
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from MedAppApi.serializers import (
    AuthPatientRegistrationSerializer,
    AuthDoctorRegistrationSerializer,
    AuthAdminStaffRegistrationSerializer,
    AppointmentSerializer
)
from MedAppApi.models import UserProfile, Patient, Doctor, Appointment



# Sample data used in tests
PATIENT_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "State",
    "zipcode": "12345",
    "date_of_birth": "1990-01-01",
    "password1": "Astrongpassword123!",
    "password2": "Astrongpassword123!",
}

DOCTOR_DATA = {
    "first_name": "Jane",
    "last_name": "Smith",
    "username": "jane_smith",
    "email": "jane@example.com",
    "phone": "1234567890",
    "specialization": "Cardiology",
    "address": "456 Elm St",
    "city": "Othertown",
    "state": "State",
    "zipcode": "54321",
    "bio": "Experienced cardiologist",
    "short_bio": "Cardiologist with 10+ years",
    "years_experience": 12,
    "password1": "Astrongpassword123!",
    "password2": "Astrongpassword123!",
}


@pytest.mark.django_db
def test_patient_registration_serializer(user_factory):
    factory = RequestFactory()
    request = factory.post('/register/patient/')
    
    # Add session to the request
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    # Instantiate the serializer with the context including the session-enabled request
    serializer = AuthPatientRegistrationSerializer(data=PATIENT_DATA, context={'request': request})
    assert serializer.is_valid(), serializer.errors

    # Save the serializer with the request
    user = serializer.save(request=request)

    assert user.userprofile.role == 'PATIENT'
    assert Patient.objects.filter(user=user).exists()
    assert Patient.objects.get(user=user).phone == PATIENT_DATA['phone']


@pytest.mark.django_db
def test_doctor_registration_serializer(user_factory, rf):
    factory = RequestFactory()
    request = factory.post('register/doctor/')

     # Add session to the request
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    
    serializer = AuthDoctorRegistrationSerializer(data=DOCTOR_DATA, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    
    user = serializer.save(request=request)

        
     
    assert user.userprofile.role == 'DOCTOR'
    # assert Doctor.objects.filter(user=user).exists()
    doctor = Doctor.objects.get(user=user)
    assert doctor.specialization == DOCTOR_DATA['specialization']
    assert doctor.years_experience == DOCTOR_DATA['years_experience']


@pytest.mark.django_db
def test_adminstaff_registration_serializer(user_factory, rf):
    
    factory = RequestFactory() 
    request = factory.post('/register/adminstaff/')

     # Add session to the request
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    serializer = AuthAdminStaffRegistrationSerializer(
        data={
            "first_name": "Alice",
            "last_name": "Johnson",
            "username": "alice_admin",
            "email": "alice@example.com",
            "title": "Office Manager",
            "password1": "Astrongpassword123!",
            "password2": "Astrongpassword123!",
        }
    )
    assert serializer.is_valid(), serializer.errors
       
    # Save the serializer with the request object 
    admin_user = serializer.save(request=request)
    
    assert UserProfile.objects.get(user=admin_user).role == "ADMIN"
    assert admin_user.adminstaff.title == "Office Manager"


@pytest.mark.django_db
def test_appointment_serializer_validation(appointment_factory, doctor_factory, patient_factory):
    doctor = doctor_factory()
    patient = patient_factory()
    appointment_data = {
        "doctor": doctor.pk,
        "patient": patient.pk,
        "date": "2024-11-10",
        "time": "14:00:00",
        "symptoms": "Mild chest pain"
    }
    
    
    serializer = AppointmentSerializer(data=appointment_data)
    assert serializer.is_valid(), serializer.errors
    appointment = serializer.save()
    
    assert appointment.date == datetime.strptime("2024-11-10", "%Y-%m-%d").date()
    assert appointment.time.strftime("%H:%M:%S") == "14:00:00"
    assert appointment.symptoms == "Mild chest pain"


@pytest.mark.django_db
def test_appointment_double_booking_validation(appointment_factory, doctor_factory, patient_factory):
    doctor = doctor_factory()
    patient = patient_factory()
    
    # Create an existing appointment at the same time
    appointment_factory(doctor=doctor, patient = patient,  date="2024-11-10", time="14:00:00")
    
    appointment_data = {
        "doctor": doctor.pk,
        "patient": patient.pk,
        "date": "2024-11-10",
        "time": "14:00:00",
        "symptoms": "Headache"
    }
    
    serializer = AppointmentSerializer(data=appointment_data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
    
    assert "This time slot is already booked for the selected doctor." in str(exc_info.value)



