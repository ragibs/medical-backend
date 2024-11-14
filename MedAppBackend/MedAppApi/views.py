from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count, F

# Custom Login View
class CustomLoginView(LoginView):
    """
    A custom login view that extends the default LoginView.
    This view adds the user's role to the response data after a successful login.
    """    
    def get_response(self):
        """
        Overrides the default get_response method to include the user's role
        in the response data.
        """        
        original_response = super().get_response()
        user = self.user 

        try:
            #SQL Equivalent: SELECT `role` FROM `medicalapp`.`medappapi_userprofile` WHERE `user_id` = user.id;
            user_profile = UserProfile.objects.get(user=user)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            role = None

        original_response.data.update({
            "role": role,
            
        })

        return original_response

# Send email function
def send_email(user):
    """
    Sends a welcome email to a newly registered user.
    """    
    subject='Welcome to Medical!'
    #SQL Equivalent: SELECT `first_name` FROM `medicalapp`.`auth_user` WHERE `id` = user.id;
    context = {
        'first_name':user.first_name,
    }
    text = render_to_string('welcome_email.txt', context=context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        # SQL Equivalent: SELECT `email` FROM `medicalapp`.`auth_user` WHERE `id` = user.id;
        to=[user.email]
    )

    message.send()

# POST Add Paitent/ Register Paitent
@api_view(['POST'])
def register_patient(request):
    """
    Register a new patient using the AuthPatientRegistrationSerializer.
    If the registration is successful, send a welcome email to the user.
    """
    serializer = AuthPatientRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save(request=request)

        send_email(user)

        return Response({
            # SQL Equivalent: SELECT `username` FROM `medicalapp`.`auth_user` WHERE `id` = user.id;
            'message': f'User {user.username} created successfully. Please try logging in with your username and password.',
            # SQL Equivalent: SELECT `id` FROM `medicalapp`.`auth_user` WHERE `id` = user.id;
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET a single Patient
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, patient_id):
    """
    Fetch details of a patient by their ID.
    Only authenticated doctors or admins can access this endpoint.
    """
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile or user_profile.role not in ['DOCTOR', 'ADMIN']:
        return Response(
            {'detail': 'You do not have permission to view this patient.'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_patient` WHERE `id` = patient_id;
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Patient.DoesNotExist:
        return Response({'detail': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET all patients
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patients(request):
    """
    Fetch a list of all patients. Only accessible by users with the 'ADMIN' role.
    """
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile or user_profile.role != 'ADMIN':
        return Response(
            {'detail': 'Only admins can get a list of all patients'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_patient`;
        patients = Patient.objects.all()

        if not patients.exists():
            return Response(
                {'detail': 'No patients registered yet'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# POST Register Doctor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_doctor(request):
    """
    Register a new doctor. Only accessible by users with the 'ADMIN' role.
    """
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only admins can register doctors', status=status.HTTP_403_FORBIDDEN)
    
    serializer = AuthDoctorRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        return Response({
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET A single doctor
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor(request, doctor_id):
    """
    Retrieve a doctor's details by their ID. Accessible to authenticated users.
    """
    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_doctor` WHERE `id` = doctor_id;
        doctor = Doctor.objects.get(id=doctor_id)
        serializer = DoctorListSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response(serializer.error_messages, status=status.HTTP_404_NOT_FOUND)

# GET all doctors 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_doctors(request):
    """
    Retrieve a list of all doctors. Access restricted to authenticated users.
    """
    # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_doctor`;
    doctors = Doctor.objects.all()
    serializer = DoctorListSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# POST Add Admin / Register Admin 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_adminstaff(request):
    """
    Endpoint to register a new admin staff member.
    Access restricted to users with the ADMIN role.
    """
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only admins can register admin staff', status=status.HTTP_403_FORBIDDEN)
    
    serializer = AuthAdminStaffRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        return Response({
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# To get avaliable slots for each doctor to generate in the frontend forms
def generate_time_slots(start_time, end_time, interval):
    """Generate all possible 30-minute time slots between start and end times."""
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    while current_time < end_datetime:
        slots.append(current_time.time())
        current_time += interval
    return slots

# GET Appointment Slots
@api_view(['GET'])
def available_slots(request, doctor_id, date):
    """
    API endpoint to get available time slots for a specific doctor on a given date.
    """
    start_time = time(9, 0)  
    end_time = time(17, 0)   
    interval = timedelta(minutes=30)

    all_slots = generate_time_slots(start_time, end_time, interval)

    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `doctor_id` = doctor_id AND `date` = 'appointment_date';
    booked_appointments = Appointment.objects.filter(doctor_id=doctor_id, date=appointment_date)
    booked_slots = [appointment.time for appointment in booked_appointments]

    available_slots = [slot.strftime("%H:%M") for slot in all_slots if slot not in booked_slots]

    return Response({"available_slots": available_slots}, status=200)

# POST Create Appointment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_appointment(request):
    """
    API to make an appointment. Only accessible by users with roles 'PATIENT' or 'ADMIN'.
    """
    user = request.user
    if hasattr(user, 'userprofile') and user.userprofile.role not in ['PATIENT', 'ADMIN']:
        return Response('You do not have permission to make an appointment', status=status.HTTP_403_FORBIDDEN)
    
    if user.userprofile.role == 'PATIENT':
        try:
            # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_patient` WHERE `user_id` = user_id;
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            return Response('Patient record not found', status=status.HTTP_400_BAD_REQUEST)
    else:
        patient_id = request.data.get('patient_id')
        if not patient_id:
            return Response('Patient ID is required for admin to make an appointment', status=status.HTTP_400_BAD_REQUEST)
        try:
            # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_patient` WHERE `id` = patient_id;
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response('Invalid patient ID', status=status.HTTP_404_NOT_FOUND)
    
    doctor_id = request.data.get('doctor_id')
    booking_date = request.data.get('booking_date')
    booking_time = request.data.get('booking_time')
    symptoms = request.data.get('symptoms')
    ai_symptoms = request.data.get('ai_summarized_symptoms')

    if not doctor_id or not booking_date or not booking_time:
        return Response('Doctor ID, booking date, and booking time are required', status=status.HTTP_400_BAD_REQUEST)

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_doctor` WHERE `id` = doctor_id;
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Invalid doctor ID', status=status.HTTP_404_NOT_FOUND)

    if Appointment.objects.filter(doctor=doctor, date=booking_date, time=booking_time).exists():
        return Response('This time slot is already booked for the selected doctor', status=status.HTTP_400_BAD_REQUEST)

    # SQL Equivalent:
    # INSERT INTO `medicalapp`.`medappapi_appointment` (`doctor_id`, `patient_id`, `date`, `time`, `symptoms`, `ai_summarized_symptoms`) 
    # VALUES (doctor_id, patient_id, 'booking_date', 'booking_time', 'symptoms', 'ai_symptoms');
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        date=booking_date,
        time=booking_time,
        symptoms=symptoms,
        ai_summarized_symptoms=ai_symptoms
    )

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def has_permission_to_delete(user, appointment):
    """
    Check if the user has permission to delete the appointment.
    - Admins can delete any appointment.
    - Doctors can delete appointments where they are assigned as the doctor.
    - Patients are not allowed to delete appointments.
    """
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.role == 'PATIENT' and appointment.patient.user == user:
        return True
    elif user_profile.role == 'DOCTOR' and appointment.doctor.user == user:
        return True
    elif user_profile.role == 'ADMIN':
        return True
    return False

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_appointment(request, appointment_id):
    """
    API to delete an appointment by its ID.
    Only admins and doctors assigned to the appointment can delete it.
    """
    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `id` = appointment_id;
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    if not has_permission_to_delete(request.user, appointment):
        return Response({"detail": "You do not have permission to delete this appointment."}, status=status.HTTP_403_FORBIDDEN)
    
    # SQL Equivalent: DELETE FROM `medicalapp`.`medappapi_appointment` WHERE `id` = appointment_id;
    appointment.delete()
    return Response({"detail": "Appointment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# GET List of appointments by Patient ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments_for_patient(request, user_id):
    """
    List all appointments for a given patient.
    - Patients can only access their own appointments.
    - Admins can access appointments for any patient.
    """
    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_patient` WHERE `user_id` = user_id;
        patient = Patient.objects.get(user__id=user_id)
    except Patient.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    if request.user != patient.user and (not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN'):
        return Response('You can only view your own appointments', status=status.HTTP_403_FORBIDDEN)

    # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `patient_id` = patient_id ORDER BY `date`, `time`;
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    serializer = ListPatientAppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

# GET List of appointments by Doctor ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments_for_doctor(request, user_id):
    """
    List all appointments for a given doctor.
    - Doctors can only access their own appointments.
    - Admins can access appointments for any doctor.
    """
    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_doctor` WHERE `user_id` = user_id;
        doctor = Doctor.objects.get(user__id=user_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    if request.user != doctor.user and (not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN'):
        return Response('You can only view your own appointments', status=status.HTTP_403_FORBIDDEN)

    # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `doctor_id` = doctor_id ORDER BY `date`, `time`;
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    serializer = ListDoctorAppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

# GET All available appointments ADMIN
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def view_all_appointments(request):
    """
    Endpoint to view all appointments.
    Accessible only by users with the 'ADMIN' role.
    """

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_userprofile` WHERE `user_id` = user_id;
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_403_FORBIDDEN)

    if user_profile.role != 'ADMIN':
        return Response({"detail": "You do not have permission to view all appointments."}, status=status.HTTP_403_FORBIDDEN)

    # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment`;
    appointments = Appointment.objects.all()

    serializer = ListAllAppointmentSerializer(appointments, many=True)

    return Response(serializer.data)

# PATCH Add/Update Notes
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_appointment_notes(request, appointment_id):
    """
    Allows a doctor to add or update notes for an existing appointment.
    """
    user = request.user

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_doctor` WHERE `user_id` = user_id;
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return Response({'detail': 'Only doctors can add notes to appointments.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `id` = appointment_id AND `doctor_id` = doctor_id;
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found or you do not have permission to modify it.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET Single appointment by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_appointment_details(request, appointment_id):
    """
    Retrieve detailed information about a specific appointment.
    Only accessible by the assigned doctor or an admin.
    """
    user = request.user

    try:
        # SQL Equivalent: SELECT * FROM `medicalapp`.`medappapi_appointment` WHERE `id` = appointment_id;
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.userprofile.role == 'ADMIN':
        pass
    elif user.userprofile.role == 'DOCTOR' and appointment.doctor.user == user:
        pass
    else:
        return Response({'detail': 'You do not have permission to view this appointment.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AppointmentDetailSerializer(appointment)

    return Response(serializer.data, status=status.HTTP_200_OK)

# GET Current and last months appointment counts based on appointment date
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_appointment_variance(request):
    """
    Get the total number of appointments for the current and last month.
    Only accessible to Admin users.
    """
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only Admins have access to view this information', status=status.HTTP_403_FORBIDDEN)
    
    current_month_start = timezone.now().date().replace(day=1)
    next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)

    # SQL Equivalent: SELECT COUNT(*) FROM `medicalapp`.`medappapi_appointment` WHERE `date` >= current_month_start AND `date` < next_month_start;
    current_monthly_count = Appointment.objects.filter(date__gte=current_month_start, date__lt=next_month_start).count()
    # SQL Equivalent: SELECT COUNT(*) FROM `medicalapp`.`medappapi_appointment` WHERE `date` >= last_month_start AND `date` < current_month_start;
    last_month_count  = Appointment.objects.filter(date__gte=last_month_start, date__lt=current_month_start).count()

    return Response({
        'current_month': current_monthly_count,
        'last_month': last_month_count
    })

# GET Monthly appointment count for each doctor   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointments_by_doctor(request):
    """
    View to get the count of appointments per doctor for the current month.
    Only accessible by Admin users.
    """
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only Admins have access to view this information', status=status.HTTP_403_FORBIDDEN)
    
    current_month_start = timezone.now().date().replace(day=1)
    next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)

    # SQL Equivalent:
    # SELECT `auth_user`.`first_name` AS `first_name`, `auth_user`.`last_name` AS `last_name`,
    # COUNT(`medappapi_appointment`.`id`) AS `appointments`
    # FROM `medicalapp`.`medappapi_appointment`
    # JOIN `medicalapp`.`medappapi_doctor` ON `medappapi_appointment`.`doctor_id` = `medappapi_doctor`.`id`
    # JOIN `medicalapp`.`auth_user` ON `medappapi_doctor`.`user_id` = `auth_user`.`id`
    # WHERE `medappapi_appointment`.`date` >= current_month_start AND `medappapi_appointment`.`date` < next_month_start
    # GROUP BY `auth_user`.`first_name`, `auth_user`.`last_name`;
    doctors_appoitment_counts = Appointment.objects.filter(
        date__gte=current_month_start,
        date__lt=next_month_start
    ).values(
        first_name=F('doctor__user__first_name'),
        last_name=F('doctor__user__last_name')
    ).annotate(appointments=Count('id'))

    response = [
        {"doctor": f"{doctor['first_name']} {doctor['last_name']}",
         "appointments": doctor['appointments']}
        for doctor in doctors_appoitment_counts]
    
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def total_patient_registrations(request):
    """
    Endpoint to get the total number of patient registrations for the current month and last month.
    Only accessible to admin users.
    """
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only Admins have access to view this information', status=status.HTTP_403_FORBIDDEN)
    
    current_month_start = timezone.now().date().replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)

    # SQL Equivalent:
    # SELECT COUNT(*) FROM `medicalapp`.`medappapi_patient` 
    # JOIN `medicalapp`.`auth_user` ON `medappapi_patient`.`user_id` = `auth_user`.`id`
    # WHERE `auth_user`.`date_joined` >= current_month_start;
    current_month_patients = Patient.objects.filter(user__date_joined__gte=current_month_start).count()

    # SQL Equivalent:
    # SELECT COUNT(*) FROM `medicalapp`.`medappapi_patient` 
    # JOIN `medicalapp`.`auth_user` ON `medappapi_patient`.`user_id` = `auth_user`.`id`
    # WHERE `auth_user`.`date_joined` >= last_month_start AND `auth_user`.`date_joined` < current_month_start;
    last_month_patients = Patient.objects.filter(user__date_joined__gte=last_month_start, user__date_joined__lt=current_month_start).count()

    return Response({
        'current_month': current_month_patients,
        'last_month': last_month_patients,
    })

# GET Today's Appointment Time Distribution
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todays_appointment_distribution(request):
    """
    Generate all possible 30-minute time slots between start and end times.
    """
    user = request.user
    if not hasattr(user, 'userprofile') or user.userprofile.role != 'ADMIN':
        return Response({"error": "You do not have permission to access this view."}, status=status.HTTP_403_FORBIDDEN)
    
    today = datetime.today().date()
    start_time = time(9, 0)
    end_time = time(17, 0)
    interval = timedelta(minutes=30)
    
    time_slots = generate_time_slots(start_time, end_time, interval)
    distribution = []

    for slot in time_slots:
        next_slot = (datetime.combine(today, slot) + interval).time()
        # SQL Equivalent: SELECT COUNT(*) FROM `medicalapp`.`medappapi_appointment` WHERE `date` = today AND `time` >= slot AND `time` < next_slot;
        count = Appointment.objects.filter(date=today, time__gte=slot, time__lt=next_slot).count()
        distribution.append({
            "time": slot.strftime("%H:%M"),
            "appointments": count
        })

    return Response(distribution)