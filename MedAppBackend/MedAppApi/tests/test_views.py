
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from MedAppApi.models import TestUser, Patient, Doctor, AdminStaff


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


def test_register_patient_method(api_client):
    url = reverse('register_patient_method')
    data = {
        'username': 'newpatient',
        'email': 'newpatient@example.com',
        'password1': 'complexpassword',
        'password2': 'complexpassword',
        'first_name': 'PatientFirstName',
        'last_name': 'PatientLastName',
        'phone': '1234567890',
        'address': '123 Main St',
        'city': 'Sample City',
        'state': 'Sample State',
        'zipcode': '12345'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data
    assert 'user_id' in response.data


def test_get_testusers(api_client):
    url = reverse('get_testusers')
    TestUser.objects.create(name='TestUser1')
    TestUser.objects.create(name='TestUser2')
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # assuming 2 test users created


def test_create_testuser(api_client):
    url = reverse('create_testuser')
    data = {'name': 'NewTestUser'}
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'NewTestUser'


def test_update_testuser(api_client):
    test_user = TestUser.objects.create(name='OriginalName')
    url = reverse('update_testuser', args=[test_user.id])
    data = {'name': 'UpdatedName'}
    
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'UpdatedName'


def test_delete_testuser(api_client):
    test_user = TestUser.objects.create(name='ToDelete')
    url = reverse('update_testuser', args=[test_user.id])
    
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert TestUser.objects.filter(id=test_user.id).count() == 0


def test_view_appointment(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
    url = reverse('view_appointment')
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Add more checks depending on what data you expect to retrieve


def test_register_doctor(api_client):
    url = reverse('register_doctor')
    data = {
        'username': 'newdoctor',
        'email': 'newdoctor@example.com',
        'password1': 'complexpassword',
        'password2': 'complexpassword',
        'first_name': 'DoctorFirstName',
        'last_name': 'DoctorLastName'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'username' in response.data
    assert response.data['username'] == 'newdoctor'
