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

# Send email function
def send_email(user):
    # # Basic Plain Text
    # send_mail(
    #     subject='Welcome to Medical!',
    #     message='Thank you for joining our platform.',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[user.email],
    #     fail_silently=True
    # )
    # Custom for rendering HTML store items configured to store under email/ images or templates
    subject='Welcome to Medical!'
    context = {
        'first_name':user.first_name,
    }
    text = render_to_string('welcome_email.txt', context=context)
    # html = render_to_string('welcome_email.html', context=context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    # message.attach_alternative(html, 'text/html')
    # # Load picture from email/images and attach to message object
    # message.attach(image)
    message.send()

# Custom Login View
class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        user = self.user  # The user who just logged in

        try:
            user_profile = UserProfile.objects.get(user=user)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            role = None

        # Add custom data to the response
        original_response.data.update({
            "role": role,
            # Add any other custom fields you want to include here
        })

        return original_response

# 🔴 Pateint Views 🔴
# 1️⃣ Add Paitent/ Register Paitent
@api_view(['POST'])
def register_patient(request):
    serializer = AuthPatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        return Response({
            'message': f'User {user.username} created successfully. Please try logging in with your username and password.',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    send_email(user)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterPatientClass(RegisterView):
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# 2️⃣ Get a single paitent
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response(serializer.error_messages, status=status.HTTP_404_NOT_FOUND)
    
# 3️⃣ Get all paitents - make sure to check the role of the auth, only admins should have acess
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patients(request):
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only admins can get a list of all patients', status=status.HTTP_403_FORBIDDEN)
    try:
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('No Patients Registered yet', status=status.HTTP_404_NOT_FOUND)
    
# 🔵 Doctor Views 🔵
# 1️⃣ Add Doctor/ Register Doctor, can only done by admin. Make sure to check role
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_doctor(request):
    # Check if the authenticated user has an admin role
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

# 2️⃣Get a single doctor - use it with doctor ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        serializer = DoctorListSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response(serializer.error_messages, status=status.HTTP_404_NOT_FOUND)

# 3️⃣ Get all doctors - can be done by only paitents and admins
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorListSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 🟡 Admin Views 🟡
# 1️⃣ Add Admin/ Register Admin - only can be done by admin
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_adminstaff(request):
    # Check if the authenticated user has an admin role
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


# ⚪️ Appointment Views ⚪️
# Helper function to generate time slots
def generate_time_slots(start_time, end_time, interval):
    """Generate time slots within a range."""
    slots = []
    while start_time < end_time:
        slots.append(start_time)
        start_time = (datetime.combine(datetime.today(), start_time) + interval).time()
    return slots

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

@api_view(['GET'])
def available_slots(request, doctor_id, date):
    # Define working hours and interval
    start_time = time(9, 0)  # Start at 9 AM
    end_time = time(17, 0)   # End at 5 PM
    interval = timedelta(minutes=30)

    # Generate all possible slots for the day
    all_slots = generate_time_slots(start_time, end_time, interval)

    # Convert the date from string to a datetime object
    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    # Query booked appointments for the doctor on the given date
    booked_appointments = Appointment.objects.filter(doctor_id=doctor_id, date=appointment_date)
    booked_slots = [appointment.time for appointment in booked_appointments]

    # Filter out booked slots
    available_slots = [slot.strftime("%H:%M") for slot in all_slots if slot not in booked_slots]

    return Response({"available_slots": available_slots}, status=200)

# 1️⃣ Create Appointment - can only be done by admin/paitent
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_appointment(request):
    # Check if the user is authenticated and has a role of either PATIENT or ADMIN
    user = request.user
    if hasattr(user, 'userprofile') and user.userprofile.role not in ['PATIENT', 'ADMIN']:
        return Response('You do not have permission to make an appointment', status=status.HTTP_403_FORBIDDEN)
    
    # Retrieve patient record if the user is a patient
    if user.userprofile.role == 'PATIENT':
        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            return Response('Patient record not found', status=status.HTTP_400_BAD_REQUEST)
    else:
        # Admin can create an appointment for any patient, so `patient_id` should be provided
        patient_id = request.data.get('patient_id')
        if not patient_id:
            return Response('Patient ID is required for admin to make an appointment', status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response('Invalid patient ID', status=status.HTTP_404_NOT_FOUND)
    
    # Required fields from request data
    doctor_id = request.data.get('doctor_id')
    booking_date = request.data.get('booking_date')
    booking_time = request.data.get('booking_time')
    symptoms = request.data.get('symptoms')
    ai_symptoms = request.data.get('ai_summarized_symptoms')

    if not doctor_id or not booking_date or not booking_time:
        return Response('Doctor ID, booking date, and booking time are required', status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the doctor
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Invalid doctor ID', status=status.HTTP_404_NOT_FOUND)

    # Check for existing appointment to prevent double-booking
    if Appointment.objects.filter(doctor=doctor, date=booking_date, time=booking_time).exists():
        return Response('This time slot is already booked for the selected doctor', status=status.HTTP_400_BAD_REQUEST)

    # Create the appointment
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        date=booking_date,
        time=booking_time,
        symptoms=symptoms,
        ai_summarized_symptoms=ai_symptoms  # Replace with actual AI summary if implemented
    )

    # Serialize and return the response
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 2️⃣ Delete an Appointment - can be done by any role
def has_permission_to_delete(user, appointment):
    """Helper function to determine if a user has permission to delete an appointment."""
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
    try:
        # Retrieve the appointment by ID
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to delete the appointment
    if not has_permission_to_delete(request.user, appointment):
        return Response({"detail": "You do not have permission to delete this appointment."}, status=status.HTTP_403_FORBIDDEN)

    # Delete the appointment
    appointment.delete()
    return Response({"detail": "Appointment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# 3️⃣ Update an Appointment - can be dony be patient and admin
# 4️⃣ Get a Single Appointment 
# 5️⃣ Get all appointments based on Doctor/Paitent ID - can be done by anyone


# getting list of appointment for patient
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments_for_patient(request, user_id):
    try:
        # Retrieve the Patient object based on the provided user_id
        patient = Patient.objects.get(user__id=user_id)
    except Patient.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is an admin or the requested patient
    if request.user != patient.user and (not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN'):
        return Response('You can only view your own appointments', status=status.HTTP_403_FORBIDDEN)

    # Get the appointments for the patient and order them by date and time
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    serializer = ListPatientAppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments_for_doctor(request, user_id):
    try:
        # Retrieve the Doctor object based on the provided user_id
        doctor = Doctor.objects.get(user__id=user_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is an admin or the requested doctor
    if request.user != doctor.user and (not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN'):
        return Response('You can only view your own appointments', status=status.HTTP_403_FORBIDDEN)

    # Get the appointments for the doctor and order them by date and time
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    serializer = ListDoctorAppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def view_all_appointments(request):
    # Get the user profile to check their role
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Return a 403 response if no user profile is found
        return Response({"detail": "User profile not found."}, status=status.HTTP_403_FORBIDDEN)

    # Check if the user is an admin
    if user_profile.role != 'ADMIN':
        # Return a 403 Forbidden if the user is not an admin
        return Response({"detail": "You do not have permission to view all appointments."}, status=status.HTTP_403_FORBIDDEN)

    # Fetch all appointments from the database
    appointments = Appointment.objects.all()

    # Serialize the appointments data
    serializer = ListAllAppointmentSerializer(appointments, many=True)

    # Return the serialized data as JSON
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_appointment_notes(request, appointment_id):
    user = request.user

    # Ensure the user is a doctor by checking the associated Doctor profile
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return Response({'detail': 'Only doctors can add notes to appointments.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Get the appointment where the logged-in doctor is the assigned doctor
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found or you do not have permission to modify it.'}, status=status.HTTP_404_NOT_FOUND)

    # Allow partial update, specifically for the notes field
    serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_appointment_details(request, appointment_id):
    user = request.user

    try:
        # Fetch the appointment by ID
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check user permissions (admin, or doctor)
    if user.userprofile.role == 'ADMIN':
        pass
    elif user.userprofile.role == 'DOCTOR' and appointment.doctor.user == user:
        pass
    else:
        return Response({'detail': 'You do not have permission to view this appointment.'}, status=status.HTTP_403_FORBIDDEN)

    # Serialize the appointment details
    serializer = AppointmentDetailSerializer(appointment)

    return Response(serializer.data, status=status.HTTP_200_OK)

# Current and last months appointment counts based on appointment date
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_appointment_variance(request):
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only Admins have access to view this information', status=status.HTTP_403_FORBIDDEN)
    
    current_month_start = timezone.now().date().replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)

    current_monthly_count = Appointment.objects.filter(date__gte=current_month_start).count()
    last_month_count  = Appointment.objects.filter(date__gte=last_month_start, date__lt=current_month_start).count()

    return Response({
        'current_month': current_monthly_count,
        'last_month': last_month_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def total_patient_registrations(request):
    # Check if the user has an admin role
    if not (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'ADMIN'):
        return Response('Only Admins have access to view this information', status=status.HTTP_403_FORBIDDEN)
    
    # Get the start of the current and last month
    current_month_start = timezone.now().date().replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)

    # Count patients registered in the current month
    current_month_patients = Patient.objects.filter(user__date_joined__gte=current_month_start).count()

    # Count patients registered in the last month
    last_month_patients = Patient.objects.filter(user__date_joined__gte=last_month_start, user__date_joined__lt=current_month_start).count()

    # Return the data as a response
    return Response({
        'current_month': current_month_patients,
        'last_month': last_month_patients,
    })

    


