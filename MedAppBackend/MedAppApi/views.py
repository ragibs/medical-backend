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
<<<<<<< HEAD
from django.contrib.auth import authenticate
=======
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, time
>>>>>>> origin/main

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
<<<<<<< HEAD
    serializer =PatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_patient_method(request):
=======
>>>>>>> origin/main
    serializer = AuthPatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        return Response({
            'message': f'User {user.username} created successfully. Please try logging in with your username and password.',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterPatientClass(RegisterView):
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# 2️⃣ Get a single paitent
@api_view(['GET'])
<<<<<<< HEAD
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

# Appointments
@api_view(['POST'])
def make_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_appointment(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def manage_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_doctors_schedule(request):
    doctor_id = request.query_params.get('doctor_id', None)
    
    if doctor_id:
        try:
            availabilities = Availability.objects.filter(doctor_id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        availabilities = Availability.objects.all()

    serializer = AvailabilitySerializer(availabilities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# Priority 2



# Nice to Haves


# Create your views here.
def home(request):
    return render(request, 'home.html', {})
# Doctor
=======
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
>>>>>>> origin/main
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
    symptoms = request.data.get('symptoms', '')

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
        ai_summarized_symptoms='jibberish'  # Replace with actual AI summary if implemented
    )

    # Serialize and return the response
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 2️⃣ Delete an Appointment - can be done by any role
# 3️⃣ Update an Appointment - can be dony be patient and admin
# 4️⃣ Get a Single Appointment 
# 5️⃣ Get all appointments based on Doctor/Paitent ID - can be done by anyone


# getting list of appointment for patient
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments_for_patient(request, patient_id):
    user = request.user
    if hasattr(user, 'userprofile') and user.userprofile.role != 'PATIENT':
        return Response('You do not have permission to view appointments', status=status.HTTP_403_FORBIDDEN)

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    serializer = AppointmentSerializer(appointments, many=True)
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
    serializer = AppointmentSerializer(appointments, many=True)

    # Return the serialized data as JSON
    return Response(serializer.data)
