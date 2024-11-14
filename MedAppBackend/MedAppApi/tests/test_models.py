import pytest
from django.utils import timezone
from datetime import date, time


@pytest.mark.django_db
class TestUserProfile:
    def test_user_profile_creation(self, user_factory, user_profile_factory):
        user = user_factory()
        profile = user_profile_factory(user=user, role='PATIENT')
        assert profile.user == user
        assert profile.role == 'PATIENT'

    def test_user_profile_roles(self, user_profile_factory):
        for role in ['PATIENT', 'DOCTOR', 'ADMIN']:
            profile = user_profile_factory(role=role)
            assert profile.role == role


@pytest.mark.django_db
class TestPatient:
    def test_patient_creation(self, patient_factory):
        patient = patient_factory()
        assert patient.phone is not None
        assert patient.address is not None


@pytest.mark.django_db
class TestDoctor:
    def test_doctor_creation(self, doctor_factory):
        doctor = doctor_factory()
        assert doctor.specialization is not None
        assert doctor.years_experience >= 1


@pytest.mark.django_db
class TestAdminStaff:
    def test_admin_staff_creation(self, admin_staff_factory):
        admin_staff = admin_staff_factory()
        assert admin_staff.title is not None


@pytest.mark.django_db
class TestAppointment:
    def test_appointment_creation(self, appointment_factory):
        appointment = appointment_factory()
        assert appointment.date == date.today()
        assert appointment.time == time(10, 0)


@pytest.mark.django_db
class TestUserActionLog:
    def test_user_action_log_creation(self, user_action_log_factory):
        log = user_action_log_factory()
        assert log.action_type is not None
        assert 200 <= log.status_code <= 500


