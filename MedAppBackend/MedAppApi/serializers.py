# Info https://www.django-rest-framework.org/tutorial/quickstart/
# rest_auth: https://dj-rest-auth.readthedocs.io/en/latest/configuration.html

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
            email= validated_data['email'],
            username= validated_data['username'],
            password= validated_data['password'],
        )
    

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor


class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        patient = Patient.objects.create(user=user, **validated_data)
        return patient
    

class AuthPatientRegistrationSerializer(RegisterSerializer):
    # User Information
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # Patient Information
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    zipcode = serializers.CharField(max_length=15)

    def custom_signup(self, request, user):
        # Alternative syntax for assigning default vals
        # user.first_name = self.validated_data.get('first_name', '')
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        patientobject_data = {
            **self.validated_data,
            'user': user,
            'appointments_booked': 0
        }

        patientobject_data.pop('username')
        patientobject_data.pop('email')
        patientobject_data.pop('password1')
        patientobject_data.pop('password2')
        patientobject_data.pop('first_name')
        patientobject_data.pop('last_name')
        Patient.objects.create(**patientobject_data)

        # Alternative Syntax for creating patient object:
        # Patient.objects.create(
        #     user=user,
        #     phone=self.validated_data['phone'],
        #     address=self.validated_data['address'],
        #     city=self.validated_data['city'],
        #     state=self.validated_data['state'],
        #     zipcode=self.validated_data['zipcode'],
        #     appointments_booked=0  # Default value for new registration
        # )


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
    years_experience = serializers.IntegerField()

    def custom_signup(self, request, user):
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        Doctor.objects.create(
            user=user,
            phone=self.validated_data['phone'],
            specialization=self.validated_data['specialization'],
            address=self.validated_data['address'],
            city=self.validated_data['city'],
            state=self.validated_data['state'],
            zipcode=self.validated_data['zipcode'],
            bio=self.validated_data['bio'],
            years_experience=self.validated_data['years_experience'],  
        )

class AuthAdminStaffRegistrationSerializer(RegisterSerializer):
    # User Information
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    # Staff Information
    title = serializers.CharField(max_length=50)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.save()

        AdminStaff.objects.create(
            user=user,
            title=self.validated_data['title'], 
        )


class AdminStaffRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        admin_staff = AdminStaff.objects.create(user=user, **validated_data)
        return admin_staff
    
class AdminStaffRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        admin_staff = AdminStaff.objects.create(user=user, **validated_data)
        return admin_staff


class PatientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDetails
        fields = '__all__'


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        


class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = '__all__'


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = '__all__'




# For Reference only serves no purpose in backend implementation
class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestUser
        fields = '__all__'