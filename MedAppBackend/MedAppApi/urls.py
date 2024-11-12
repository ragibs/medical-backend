from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # Authentication and Registration
    # ---------------------------------
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # User Registration Endpoints (Admin Access)
    path('register/patient/', register_patient, name='register_patient'),
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('register/adminstaff/', register_adminstaff, name='register_adminstaff'),

    # Patient Management
    # ---------------------------------
    path('getpatient/<int:patient_id>/', get_patient, name='get_patient'),  # Retrieve a specific patient
    path('getpatients/', list_patients, name='list_patients'),  # List all patients

    # Doctor Management
    # ---------------------------------
    path('getdoctor/<int:doctor_id>/', get_doctor, name='get_doctor'),  # Retrieve a specific doctor
    path('getdoctors/', list_doctors, name='list_doctors'),  # List all doctors

    # Appointment Management
    # ---------------------------------
    path('make/appointment/', make_appointment, name='make_appointment'),  # Create an appointment
    path('deleteappointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),  # Delete an appointment
    path('appointments/<int:appointment_id>/add-notes/', views.add_appointment_notes, name='add_appointment_notes'),  # Add notes to an appointment
    path('appointments/<int:appointment_id>/', view_appointment_details, name='view_appointment_details'),  # View appointment details

    # Appointment Slots (Doctor-specific)
    # ---------------------------------
    path('doctors/<int:doctor_id>/available-slots/<str:date>/', available_slots, name='available_slots'),

    # Appointment Views for Users
    # ---------------------------------
    path('view/patient-appointment/<int:user_id>/', list_appointments_for_patient, name='list_appointments_for_patient'),  # View appointments for a specific patient
    path('view/doctor-appointment/<int:user_id>/', list_appointments_for_doctor, name='list_appointments_for_doctor'),  # View appointments for a specific doctor
    path('view/all-appointments/', views.view_all_appointments, name='view_all_appointments'),  # Admin can view all appointments

    # Dashboard Analytics
    # ---------------------------------
    path('appointment/changecount/', monthly_appointment_variance, name='monthly_appointment_variance'),  # Monthly appointment comparison
    path('appointment/countbydoctor/', appointments_by_doctor, name='appointments_by_doctor'),  # Count appointments by doctor for the current month
    path('registrations/', total_patient_registrations, name='total_patient_registrations'),  # Patient registrations count (current vs. last month)
    path('appointment/today-count/', todays_appointment_distribution, name='todays_appointment_distribution'),  # Today's appointment distribution by time slots
]