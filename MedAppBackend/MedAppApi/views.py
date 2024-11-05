from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import RegisterView
from .models import *
from .serializers import *
from django.contrib.auth import authenticate


# Priority 1
# Register Patient
@api_view(['POST'])
def register_patient(request):
    serializer =PatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_patient_method(request):
    serializer = AuthPatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterPatientClass(RegisterView):
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# Login for all user types
@api_view(['GET'])
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
@api_view(['POST'])
def register_doctor(request):
    pass

@api_view(['GET'])
def get_doctors(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def update_doctor(request, pk):
    pass

@api_view(['POST'])
def update_availability(request):
    pass

# Patient
@api_view(['POST'])
def register_patient(request):
    pass

@api_view(['GET'])
def get_patients(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def update_patient(request, pk):
    pass

# Admin Staff
@api_view(['POST'])
def register_admninstaff(request):
    pass

@api_view(['GET'])
def get_adminstaff(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def update_adminstaff(request, pk):
    pass

# Appointments
@api_view(['POST'])
def make_appointment(request):
    pass

@api_view(['GET'])
def view_appointment(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def manage_appointment(request, pk):
    pass

# Ratings
@api_view(['POST'])
def create_rating(request):
    pass

@api_view(['GET'])
def view_rating(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def update_rating(request, pk):
    pass

# Testimonials
@api_view(['POST'])
def create_testimonial(request):
    pass

@api_view(['GET'])
def view_testimonial(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def update_testimonial(request, pk):
    pass




# API views
# @api_view(['GET'])
# def get_doctor(request):
#     return Response(DoctorSerializer())

@api_view(['GET'])
def get_testusers(request):
    users = TestUser.objects.all()
    serializer = TestUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_testuser(request):
    serializer = TestUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def update_testuser(request, pk):
    try:
        user = TestUser.objects.get(pk=pk)
    except TestUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TestUserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TestUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
