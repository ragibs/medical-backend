from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import RegisterView
from .models import *
from .serializers import *


# Priority 1
# Register Patient
@api_view(['POST'])
def register_patient(request):
    pass

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
    
# Register doctors
@api_view(['POST'])
def register_doctor(request):
    serializer = AuthDoctorRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Register Admin
@api_view(['POST'])
def register_adminstaff(request):
    serializer = AuthAdminStaffRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def make_appointment(request):
    if not request.user.is_authenticated:
        return Response('Must be logged in', status=status.HTTP_401_UNAUTHORIZED)
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return Response('Not a valid patient', status=status.HTTP_400_BAD_REQUEST)
    
    doctor_id = request.data.get('doctor_id')
    booking_date = request.data.get('booking_date')

    if not doctor_id or booking_date:
        return Response('Insufficient information', status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Invalid doctor ID', status=status.HTTP_404_NOT_FOUND)
    
    appointment = Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        symptom_summary ='jibberish',
        booking_date=booking_date
    )

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# Login for all user types
@api_view(['GET'])
def login(request):
    pass

# Appointments


@api_view(['GET'])
def view_appointment(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def manage_appointment(request, pk):
    pass

@api_view(['GET'])
def get_doctors(request):
    pass


@api_view(['GET'])
def view_doctors_schedule(request):
    pass



# Priority 2



# Nice to Haves


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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
