# MedAppBackend/MedAppApi/tests/conftest.py

import pytest
from rest_framework.test import APIClient
from .factories import (
    UserFactory,
    UserProfileFactory,
    DoctorFactory,
    PatientFactory,
    AdminStaffFactory,
    AppointmentFactory,
    UserActionLogFactory
)

# Setup an APIClient instance for the tests
@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def user_profile_factory():
    return UserProfileFactory

@pytest.fixture
def doctor_factory():
    return DoctorFactory

@pytest.fixture
def patient_factory():
    return PatientFactory

@pytest.fixture
def admin_staff_factory():
    return AdminStaffFactory

@pytest.fixture
def appointment_factory():
    return AppointmentFactory

@pytest.fixture
def user_action_log_factory():
    return UserActionLogFactory
