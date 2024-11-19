import pytest
import json
from django.contrib.auth.models import User
from io import BytesIO
from django.http import HttpRequest, JsonResponse
from django.test import RequestFactory
from django.test import Client
from rest_framework.test import APIClient
from MedAppApi.models import UserActionLog
from MedAppApi.middleware import ActionLoggingMiddleware
from django.urls import reverse




@pytest.mark.django_db
def test_logging_middleware_get_request(user_factory):
    # Set up an authenticated user
    user = user_factory(username = 'testuser')
    user.set_password('Str0ngP@ssw0rd!')
    user.save()
   
    factory = RequestFactory() 
    request = factory.get('register/patient/') 
    request.META['REMOTE_ADDR'] = '127.0.0.1' 
    request.user = user

    # Print request path to debug 
    print(f"Request path: {request.path}")

    # Initialize middleware with a mock get_response callable 
    def get_response(request):
        return JsonResponse({'detail': 'OK'}, status=200) 
    
    middleware = ActionLoggingMiddleware(get_response)

    # Process the request 
    response = middleware(request)
    


    # Validate that the action log was created with correct data
    log_entry = UserActionLog.objects.last()

    # Print log entry endpoint to debug 
    print(f"Log entry endpoint: {log_entry.endpoint}")


    assert log_entry.user == user
    assert log_entry.action_type == 'VIEW'


    assert log_entry.endpoint == '/registerpatient/'
    assert log_entry.status_code == 200
    assert log_entry.outcome == 'PASS'



@pytest.mark.django_db
def test_logging_middleware_anonymous_user(api_client):
    # Send a GET request as an anonymous user to an existing endpoint
    response = api_client.get(reverse('list_doctors'))
    
    # Check response status (likely 401 Unauthorized or 403 Forbidden)
    assert response.status_code in [401, 403]
    
    # Check that a UserActionLog entry was created with user=None
    log_entry = UserActionLog.objects.last()
    assert log_entry.user is None
    assert log_entry.action_type == 'VIEW'
    assert log_entry.endpoint == reverse('list_doctors')
    assert log_entry.status_code in [401, 403]
    assert log_entry.outcome == 'FAIL'



@pytest.mark.django_db
def test_logging_middleware_invalid_json(user_factory):
    user = user_factory(username='testuser')
    user.set_password('Str0ngP@ssw0rd!')
    user.save()
    
    factory = RequestFactory() 
    request = factory.post(reverse('register_patient'))
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    request.user = user
    request._stream = BytesIO(b'invalid json')  # Set invalid JSON using BytesIO
    
    # Initialize middleware with a mock get_response callable
    def get_response(request):
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)

    middleware = ActionLoggingMiddleware(get_response)

    # Call middleware to process the request
    response = middleware(request)

    # Check response status
    assert response.status_code >= 400

    # Validate that invalid JSON data was handled and logged correctly
    log_entry = UserActionLog.objects.last()
    assert log_entry.user == user
    assert log_entry.endpoint == '/register/patient/'
    assert log_entry.status_code == response.status_code
    assert log_entry.outcome == 'FAIL'
    assert "Invalid JSON" in log_entry.details
