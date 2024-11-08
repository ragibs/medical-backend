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
    
    #Doctor endpoint
    path('getdoctors/', list_doctors, name='list_doctors'),

    # Appointment endpoint
    path('make/appointment/', make_appointment, name='make_appointment'),
    path('doctors/<int:doctor_id>/available-slots/<str:date>/', available_slots, name='available_slots')

]