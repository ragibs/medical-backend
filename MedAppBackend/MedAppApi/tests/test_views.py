import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.request import Request
from datetime import datetime, time
from MedAppApi.models import Appointment
from MedAppApi.views import register_patient


# Test Custom Login View
@pytest.mark.django_db
def test_custom_login_view(api_client, user_factory, user_profile_factory):
    user = user_factory(username='testuser')
    user.set_password('Str0ngP@ssw0rd!')
    user.save()
   
    # Create user profile with role 'PATIENT'
    user_profile_factory(user=user, role='PATIENT')
    
    # Prepare login data
    login_data = {
        'username': 'testuser',
        'password': 'Str0ngP@ssw0rd!'
    }
    
    # Make POST request to login endpoint with credentials
    response = api_client.post(reverse('login'), data=login_data, format='json')
    
    # Assert the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK, f"Expected status 200, got {response.status_code}"
    
    # Assert that 'role' is present in the response data
    assert 'role' in response.data, "Response does not contain 'role'"
    
    # Assert that the role is 'PATIENT'
    assert response.data['role'] == 'PATIENT', f"Expected role 'PATIENT', got {response.data['role']}"



# Test Get Patient (Permission Test)
@pytest.mark.django_db
def test_get_patient_permission(api_client, user_factory, user_profile_factory, patient_factory):
    doctor_user = user_factory(username='doctor')
    doctor_profile = user_profile_factory(user=doctor_user, role='DOCTOR')
    patient = patient_factory()
    api_client.force_authenticate(user=doctor_user)

    response = api_client.get(reverse('get_patient', args=[patient.id]))
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == patient.id


# Test List Patients (Admin Only)
@pytest.mark.django_db
def test_list_patients_admin_only(api_client, user_factory, user_profile_factory, patient_factory):
    admin_user = user_factory(username='admin')
    admin_profile = user_profile_factory(user=admin_user, role='ADMIN')
    api_client.force_authenticate(user=admin_user)

     # Create patients
    patient1 = patient_factory()
    patient2 = patient_factory()

    response = api_client.get(reverse('list_patients'))
    
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) >= 2
    assert any(patient['id'] == patient1.id for patient in response.data)
    assert any(patient['id'] == patient2.id for patient in response.data)



# Test Register Doctor (Admin Only)
@pytest.mark.django_db
def test_register_doctor(api_client, user_factory, user_profile_factory):
    admin_user = user_factory(username='testuser')
    admin_user.set_password('Str0ngP@ssw0rd!')
    admin_user.save()
    admin_profile = user_profile_factory(user=admin_user, role='ADMIN')
    api_client.force_authenticate(user=admin_user)

    doctor_data = {
        "username": "newdoctor",
        "email": "johnsmith@example.com",
        "password1": "securepassword123", # why are two passwords required here.
        "password2": "securepassword123",
        "first_name": "John",
        "last_name": "Smith",
        "phone": "213-555-1010", 
        "specialization": "Cardiology",
        "address": "123 Heartbeat Lane",
        "city": "Los Angeles",
        "state": "CA",
        "zipcode": "90001",
        "bio": "Dr. John Smith has over 15 years of experience in cardiology. Previously worked at Cedars-Sinai Medical Center and specializes in treating heart conditions and performing complex surgeries.",
        "short_bio": "Cardiologist with 15 years experience",
        "years_experience": 15
    }

    response = api_client.post(reverse('register_doctor'), data = doctor_data, format = 'json')

 
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == 'newdoctor'



# Test Available Appointment Slots
@pytest.mark.django_db
def test_available_slots(api_client, doctor_factory, appointment_factory):
    doctor = doctor_factory()
    date_str = datetime.today().strftime('%Y-%m-%d')

    # Create an appointment to book a slot
    appointment_factory(
        doctor=doctor,
        date=datetime.today().date(),
        time=datetime.strptime('09:30', '%H:%M').time()
    )

    response = api_client.get(reverse('available_slots', args=[doctor.id, date_str]))
    
    assert response.status_code == status.HTTP_200_OK
    assert 'available_slots' in response.data
    
    # Check that '09:30' is not in available slots
    assert '09:30' not in response.data['available_slots']


# Test Make Appointment
@pytest.mark.django_db
def test_make_appointment(api_client, user_factory, user_profile_factory, doctor_factory, patient_factory):
    patient_user = user_factory(username='patient')
    patient_profile = user_profile_factory(user=patient_user, role='PATIENT')
    patient = patient_factory(user=patient_user)
    doctor = doctor_factory()
    
    api_client.force_authenticate(user=patient_user)

    data = {
        'doctor_id': doctor.id,
        'booking_date': '2024-12-01',
        'booking_time': '10:30',
        'symptoms': 'Cough and fever'
    }

    response = api_client.post(reverse('make_appointment'), data, format = 'json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['doctor'] == doctor.id



# Test Delete Appointment
@pytest.mark.django_db
def test_delete_appointment(api_client, user_factory, user_profile_factory, doctor_factory, appointment_factory):
    # Create an admin user
    admin_user = user_factory(username='admin')
    admin_user.set_password('Adm1nStr0ngP@ss!')
    admin_user.save()
    user_profile_factory(user=admin_user, role='ADMIN')
    
    # Create a doctor
    doctor = doctor_factory()
    
    # Create an appointment
    appointment = appointment_factory(doctor=doctor)
    
    # Authenticate as admin
    api_client.force_authenticate(user=admin_user)
    
    response = api_client.delete(
        reverse('delete_appointment', args=[appointment.id])
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Appointment.objects.filter(id=appointment.id).exists()

# Test List Appointments for Patient
@pytest.mark.django_db
def test_list_appointments_for_patient(api_client, user_factory, user_profile_factory, patient_factory, appointment_factory):
    patient_user = user_factory(username='patient')
    patient_user.set_password('PatStr0ngP@ss!')
    patient_user.save()
    user_profile_factory (user=patient_user, role='PATIENT')
    patient = patient_factory(user=patient_user)

    # Create appointments
    appointment1 = appointment_factory(patient=patient)
    appointment2 = appointment_factory(patient=patient)

    api_client.force_authenticate(user=patient.user)
    response = api_client.get(reverse('list_appointments_for_patient', args=[patient.user.id]))
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 2
    
    # check specific appointments are in the response
    appointment_ids = [appointment1.id, appointment2.id]
    response_ids = [appt['id'] for appt in response.data]
    for appt_id in appointment_ids:
        assert appt_id in response_ids


# Test List Appointments for Doctor
@pytest.mark.django_db
def test_list_appointments_for_doctor(api_client, doctor_factory, appointment_factory):
    doctor = doctor_factory()
    appointment_factory(doctor=doctor)

    # Create appointments
    appointment1 = appointment_factory(doctor=doctor)
    appointment2 = appointment_factory(doctor=doctor)

    api_client.force_authenticate(user=doctor.user)
    response = api_client.get(reverse('list_appointments_for_doctor', args=[doctor.user.id]))
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 2

    # check specific appointments are in the response
    appointment_ids = [appointment1.id, appointment2.id]
    response_ids = [appt['id'] for appt in response.data]
    for appt_id in appointment_ids:
        assert appt_id in response_ids


