import pytest
from django.contrib.auth.models import User
from MedAppApi.models import Doctor, AdminStaff, Patient, BasicPatient, ProPatient, PatientDetails, Appointment, Testimonials, Ratings, TestUser


@pytest.mark.django_db
def test_doctor_creation():
    user = User.objects.create(username="doctoruser")
    doctor = Doctor.objects.create(
        user=user,
        phone="1234567890",
        specialization="Cardiologist",
        address="123 Medical St",
        city="MedCity",
        state="MedState",
        zipcode="12345",
        bio="Experienced cardiologist.",
        years_experience=15
    )
    assert doctor.user == user
    assert doctor.specialization == "Cardiologist"
    assert doctor.years_experience == 15


@pytest.mark.django_db
def test_admin_staff_creation():
    user = User.objects.create(username="adminstaffuser")
    admin_staff = AdminStaff.objects.create(
        user=user,
        title="Receptionist"
    )
    assert admin_staff.user == user
    assert admin_staff.title == "Receptionist"


@pytest.mark.django_db
def test_patient_creation():
    user = User.objects.create(username="patientuser")
    patient = Patient.objects.create(
        user=user,
        phone="9876543210",
        address="456 Patient Rd",
        city="HealCity",
        state="HealState",
        zipcode="67890",
        appointments_booked=5
    )
    assert patient.user == user
    assert patient.appointments_booked == 5


@pytest.mark.django_db
def test_basic_patient_creation():
    user = User.objects.create(username="basicpatientuser")
    patient = BasicPatient.objects.create(
        user=user,
        phone="1112223333",
        address="789 Basic St",
        city="BasicCity",
        state="BasicState",
        zipcode="33333",
        appointments_booked=3,
        maximum_appointments=100
    )
    assert patient.maximum_appointments == 100


@pytest.mark.django_db
def test_pro_patient_creation():
    user = User.objects.create(username="propatientuser")
    patient = ProPatient.objects.create(
        user=user,
        phone="4445556666",
        address="101 Pro Rd",
        city="ProCity",
        state="ProState",
        zipcode="44444",
        appointments_booked=10,
        maximum_appointments=99999999
    )
    assert patient.maximum_appointments == 99999999


@pytest.mark.django_db
def test_patient_details_creation():
    user = User.objects.create(username="patientdetailsuser")
    patient = Patient.objects.create(
        user=user,
        phone="1234567890",
        address="123 Heal Rd",
        city="Cityville",
        state="Stateland",
        zipcode="12345",
        appointments_booked=2
    )
    patient_details = PatientDetails.objects.create(
        patient=patient,
        age=30,
        sex="Male",
        weight=70,
        height=180,
        history="No prior history."
    )
    assert patient_details.age == 30
    assert patient_details.sex == "Male"


@pytest.mark.django_db
def test_appointment_creation():
    doctor_user = User.objects.create(username="doctor")
    patient_user = User.objects.create(username="patient")
    doctor = Doctor.objects.create(user=doctor_user, phone="5555555555", specialization="Surgeon", address="123 Doc Rd", city="DocCity", state="DocState", zipcode="54321", bio="Experienced Surgeon", years_experience=10)
    patient = Patient.objects.create(user=patient_user, phone="6666666666", address="456 Patient Rd", city="PatientCity", state="PatientState", zipcode="65432", appointments_booked=1)
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        symptom_summary="Chest pain and fatigue",
        booking_date="2024-11-06 09:00:00",
        cost=100.00
    )
    assert appointment.symptom_summary == "Chest pain and fatigue"
    assert appointment.cost == 100.00


@pytest.mark.django_db
def test_testimonial_creation():
    user = User.objects.create(username="testimonialuser")
    testimonial = Testimonials.objects.create(
        user=user,
        testimonial="Great service and friendly staff!"
    )
    assert testimonial.testimonial == "Great service and friendly staff!"


@pytest.mark.django_db
def test_rating_creation():
    doctor_user = User.objects.create(username="doctorrating")
    patient_user = User.objects.create(username="patientrating")
    doctor = Doctor.objects.create(user=doctor_user, phone="9999999999", specialization="Dermatologist", address="123 Skin St", city="SkinCity", state="SkinState", zipcode="33333", bio="Skin specialist", years_experience=12)
    patient = Patient.objects.create(user=patient_user, phone="8888888888", address="789 Wellness Rd", city="WellnessCity", state="WellState", zipcode="22222", appointments_booked=1)
    rating = Ratings.objects.create(
        patient=patient,
        doctor=doctor,
        rating=5
    )
    assert rating.rating == 5


@pytest.mark.django_db
def test_testuser_creation():
    test_user = TestUser.objects.create(
        name="Sample User",
        age=30
    )
    assert str(test_user) == "Name:Sample User Age:30"
    assert test_user.age == 30
