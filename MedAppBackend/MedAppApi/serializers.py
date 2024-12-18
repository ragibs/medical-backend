from datetime import datetime
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
        # SQL Equivalent: SELECT EXISTS (SELECT 1 FROM `medicalapp`.`auth_user` WHERE `auth_user`.`username` = username);
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, email):
        # SQL Equivalent: SELECT EXISTS (SELECT 1 FROM `medicalapp`.`auth_user` WHERE `auth_user`.`username` = username);
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def custom_signup(self, request, user):
        # Set user's first and last name
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        # SQL Equivalent for user Creation:
        # INSERT INTO `medicalapp`.`auth_user` (`first_name`, `last_name`, `username`, `email`, `password`)
        # VALUES (validated_data['first_name'], validated_data['last_name'], validated_data['username'], validated_data['email'], validated_data['password']);
        user.save()

        # Create the profile with role
        # SQL Equivalent: # INSERT INTO `medicalapp`.`medappapi_userprofile` (`user_id`, `role`) VALUES (user.id, 'PATIENT');
        UserProfile.objects.create(user=user, role='PATIENT')

        # Create the patient model instance
        # SQL Equivalent for Patient Creation:
        # INSERT INTO `medicalapp`.`medappapi_patient` (`phone`, `address`, `city`, `state`, `zipcode`, `user_id`, `date_of_birth`) 
        # VALUES (validated_data[phone], validated_data[address], validated_data[city], validated_data[state], validated_data[zipcode], user.id, validated_data[date_of_birth]);
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
        # SQL Equivalent for user Creation:
        # INSERT INTO `medicalapp`.`auth_user` (`first_name`, `last_name`, `username`, `email`, `password`)
        # VALUES (validated_data['first_name'], validated_data['last_name'], validated_data['username'], validated_data['email'], validated_data['password']);
        user.save()

        # Create a UserProfile for role management
        # SQL Equivalent: # INSERT INTO `medicalapp`.`medappapi_userprofile` (`user_id`, `role`) VALUES (user.id, 'DOCTOR');
        UserProfile.objects.create(user=user, role='DOCTOR')

        # Create a Doctor instance
        # SQL Equivalent for Doctor Creation:
        # INSERT INTO `medicalapp`.`medappapi_doctor` (`phone`, `specialization`, `address`, `city`, `state`, `zipcode`, `bio`, `short_bio`, `years_experience`, `user_id`) 
        # VALUES (validated_data[phone], validated_data[specialization], validated_data[address], validated_data[city], validated_data[state], validated_data[zipcode], validated_data[bio], validated_data[short_bio], validated_data[years_experience], user.id);
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
        # SQL Equivalent for user Creation:
        # INSERT INTO `medicalapp`.`auth_user` (`first_name`, `last_name`, `username`, `email`, `password`)
        # VALUES (validated_data['first_name'], validated_data['last_name'], validated_data['username'], validated_data['email'], validated_data['password']);
        user.save()

        # Create a UserProfile for role management
        # SQL Equivalent: # INSERT INTO `medicalapp`.`medappapi_userprofile` (`user_id`, `role`) VALUES (user.id, 'ADMIN');
        UserProfile.objects.create(user=user, role='ADMIN')

        # Create an AdminStaff instance
        # SQL Equivalent for Admin Creation:
        # INSERT INTO `medicalapp`.`medappapi_adminstaff` (`title`, `user_id`) 
        # VALUES (validated_data[title], user.id);
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
        # SQL Equivalent: SELECT EXISTS (SELECT 1 FROM `medicalapp`.`medappapi_appointment` WHERE `doctor_id` = data.get('doctor') AND `date` = data.get('date') AND `time` = data.get('time'));
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError("This time slot is already booked for the selected doctor.")

        return data
    
 # Getting the list of all doctors   
class DoctorListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'short_bio', 'bio', 'email']

class PatientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'email']

class ListPatientAppointmentSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor_full_name',
            'date',
            'time'
        ]

    # SQL Equivalent:
    # SELECT CONCAT(`auth_user`.`first_name`, ' ', `auth_user`.`last_name`) AS doctor_full_name
    # FROM `medicalapp`.`medappapi_appointment`
    # JOIN `medicalapp`.`medappapi_doctor` ON `medappapi_appointment`.`doctor_id` = `medappapi_doctor`.`id`
    # JOIN `medicalapp`.`auth_user` ON `medappapi_doctor`.`user_id` = `auth_user`.`id`
    # WHERE `medappapi_appointment`.`id` = obj.id;
    def get_doctor_full_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        if 'time' in representation and representation['time']:
            representation['time'] = datetime.strptime(representation['time'], "%H:%M:%S").strftime("%I:%M %p")
        return representation

class ListDoctorAppointmentSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient_full_name',
            'date',
            'time',
            'ai_summarized_symptoms',
        ]

    # SQL Equivalent:
    # SELECT CONCAT(`auth_user`.`first_name`, ' ', `auth_user`.`last_name`) AS patient_full_name
    # FROM `medicalapp`.`medappapi_appointment`
    # JOIN `medicalapp`.`medappapi_patient` ON `medappapi_appointment`.`patient_id` = `medappapi_patient`.`id`
    # JOIN `medicalapp`.`auth_user` ON `medappapi_patient`.`user_id` = `auth_user`.`id`
    # WHERE `medappapi_appointment`.`id` = obj.id;
    def get_patient_full_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        if 'time' in representation and representation['time']:
            representation['time'] = datetime.strptime(representation['time'], "%H:%M:%S").strftime("%I:%M %p")
        return representation

class ListAllAppointmentSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.SerializerMethodField()
    doctor_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient_full_name',
            'doctor_full_name',
            'date',
            'time',
            'ai_summarized_symptoms',
        ]

    def get_patient_full_name(self, obj):
        # Check if patient and user are available
        if obj.patient and obj.patient.user:
            return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
        return "Unknown Patient"

    def get_doctor_full_name(self, obj):
        # Check if doctor and user are available
        if obj.doctor and obj.doctor.user:
            return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
        return "Unknown Doctor"

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        if 'time' in representation and representation['time']:
            try:
                representation['time'] = datetime.strptime(
                    representation['time'], "%H:%M:%S"
                ).strftime("%I:%M %p")
            except ValueError:
                representation['time'] = "Invalid time format"
        return representation
    


class AppointmentDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    ai_summarized_symptoms = serializers.CharField(allow_blank=True)
    notes = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()

    class Meta:
        model = Appointment
        fields = [
            'patient_name', 
            'doctor_name', 
            'date', 
            'time', 
            'symptoms', 
            'ai_summarized_symptoms', 
            'notes', 
            'created_at'
        ]

    def get_patient_name(self, obj):
        if obj.patient and obj.patient.user:
            return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
        return "Unknown Patient"

    def get_doctor_name(self, obj):
        if obj.doctor and obj.doctor.user:
            return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
        return "Unknown Doctor"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Format the 'time' field to "11:30 AM"
        if 'time' in representation and representation['time']:
            try:
                representation['time'] = datetime.strptime(
                    representation['time'], "%H:%M:%S"
                ).strftime("%I:%M %p")
            except ValueError:
                representation['time'] = "Invalid Time"
                
        return representation
    