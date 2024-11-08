# Info https://www.django-rest-framework.org/tutorial/quickstart/
# rest_auth: https://dj-rest-auth.readthedocs.io/en/latest/configuration.html

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer

#PaitentAuth
class AuthPatientRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    zipcode = serializers.CharField(max_length=15)
    date_of_birth = serializers.DateField(required=True)


    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def custom_signup(self, request, user):
        # Set user's first and last name
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        # Create the profile with role
        UserProfile.objects.create(user=user, role='PATIENT')

        # Create the patient model instance
        Patient.objects.create(
            user=user,
            phone=self.validated_data['phone'],
            address=self.validated_data['address'],
            city=self.validated_data['city'],
            state=self.validated_data['state'],
            zipcode=self.validated_data['zipcode'],
            date_of_birth=self.validated_data['date_of_birth'],
        )
# Doctor Auth
class AuthDoctorRegistrationSerializer(RegisterSerializer):
    # User Information
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # Doctor Information
    phone = serializers.CharField(max_length=15)
    specialization = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    zipcode = serializers.CharField(max_length=15)
    bio = serializers.CharField()
    short_bio = serializers.CharField(max_length=150)
    years_experience = serializers.IntegerField()

    def custom_signup(self, request, user):
        # Set the user's first and last name
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        # Create a UserProfile for role management
        UserProfile.objects.create(user=user, role='DOCTOR')

        # Create a Doctor instance
        Doctor.objects.create(
            user=user,
            phone=self.validated_data['phone'],
            specialization=self.validated_data['specialization'],
            address=self.validated_data['address'],
            city=self.validated_data['city'],
            state=self.validated_data['state'],
            zipcode=self.validated_data['zipcode'],
            bio=self.validated_data['bio'],
            short_bio=self.validated_data['short_bio'],
            years_experience=self.validated_data['years_experience'],
        )

# Admin Staff Registration Serializer
class AuthAdminStaffRegistrationSerializer(RegisterSerializer):
    # User Information
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # Staff Information
    title = serializers.CharField(max_length=50)

    def custom_signup(self, request, user):
        # Set the user's first and last name
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        # Create a UserProfile for role management
        UserProfile.objects.create(user=user, role='ADMIN')

        # Create an AdminStaff instance
        AdminStaff.objects.create(
            user=user,
            title=self.validated_data['title'],
        )
#Creating Appointment 
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'date',
            'time',
            'symptoms',
            'ai_summarized_symptoms',
            'notes',
        ]
        read_only_fields = ['ai_summarized_symptoms']  # Set this field as read-only

    def validate(self, data):
        # Custom validation for time slots, preventing double-booking for the same doctor
        doctor = data.get('doctor')
        date = data.get('date')
        time = data.get('time')

        # Check if there's already an appointment for the doctor at the same date and time
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError("This time slot is already booked for the selected doctor.")

        return data
    
 # Getting the list of all doctors   
class DoctorListSerializer(serializers.ModelSerializer):
    # fecthing from the user model
    id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'short_bio', 'bio']

 # Getting the list of all doctors   
class PatientSerializer(serializers.ModelSerializer):
    # fecthing from the user model
    id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone', 'address']