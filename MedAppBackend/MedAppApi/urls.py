from django.urls import path, include
from dj_rest_auth.views import LoginView
from . import views
from .views import *

urlpatterns = [
    # Placeholder
    path('', views.home, name='home'),
    path('testusers/', get_testusers, name='get_testusers'),
    path('testusers/create/', create_testuser, name='create_testuser'),
    path('testusers/<int:pk>', update_testuser, name='update_testuser'),
    path('login', LoginView.as_view(), name='login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('register/patient/method', register_patient_method, name='register_patient_method'),
    path('register/patient/class', RegisterPatientClass.as_view(), name='register_patient_class'),
    path('register/doctor', register_doctor, name='register_doctor'),
    path('register/adminstaff', register_adminstaff, name='register_adminstaff'),
    path('make/appointment', make_appointment, name='make_appointment'),
]