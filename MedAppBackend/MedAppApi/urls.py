from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Registration endpoints
    path('register/patient/', register_patient, name='register_patient'),
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('register/adminstaff/', register_adminstaff, name='register_adminstaff'),

    # Patient endpoint
    path('getpatient/<int:patient_id>', get_patient, name='get_patient'),
    path('getpatients/', list_patients, name='list_patients'),
    
    #Doctor endpoint
    path('getdoctors/', list_doctors, name='list_doctors'),
    path('getdoctor/<int:doctor_id>', get_doctor, name='get_doctor'),

    # Appointment endpoint
    path('make/appointment/', make_appointment, name='make_appointment'),
    path('doctors/<int:doctor_id>/available-slots/<str:date>/', available_slots, name='available_slots'),
    path('deleteappointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),

    path('view/patient-appointment/<int:user_id>/', list_appointments_for_patient, name='list_appointments_for_patient'),
    path('view/doctor-appointment/<int:user_id>/', list_appointments_for_doctor, name='list_appointments_for_doctor'),
    path('view/all-appointments/', views.view_all_appointments, name='view_all_appointments'),
    path('appointments/<int:appointment_id>/add-notes/', views.add_appointment_notes, name='add_appointment_notes'),
    path('appointments/<int:appointment_id>/', view_appointment_details, name='view_appointment_details'),
    path('appointment/changecount/', monthly_appointment_variance, name='monthly_appointment_variance'),
    path('appointment/countbydoctor/', appointments_by_doctor, name='appointments_by_doctor'),
    path('registrations/', total_patient_registrations, name='total_patient_registrations'),
    path('appointment/today-count/', todays_appointment_distribution, name='todays_appointment_distribution'),

]