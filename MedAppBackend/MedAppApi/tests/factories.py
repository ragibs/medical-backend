import factory
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from MedAppApi.models import UserProfile, Patient, Doctor, AdminStaff, Appointment, UserActionLog
from django.utils import timezone
from datetime import date, time


fake  = Faker()
# User Factory for testing
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n:04}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.LazyFunction(lambda: make_password('password'))


# UserProfile Factory
class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    role = factory.Iterator(['PATIENT', 'DOCTOR', 'ADMIN'])


# Patient Factory
class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserFactory)
    # phone = factory.Faker('phone_number')
    phone = factory.LazyFunction(lambda: ''.join(fake.random_elements('0123456789', 10)))
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    zipcode = factory.Faker('postcode')
    date_of_birth = factory.Faker('date_of_birth')


# Doctor Factory
class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor

    user = factory.SubFactory(UserFactory)
    # phone = factory.Faker('phone_number')
    phone = factory.LazyFunction(lambda: ''.join(fake.random_elements('0123456789', 10)))
    specialization = factory.Faker('job')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    zipcode = factory.Faker('postcode')
    bio = factory.Faker('paragraph')
    short_bio = factory.Faker('sentence')
    years_experience = factory.Faker('random_int', min=1, max=40)


# AdminStaff Factory
class AdminStaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdminStaff

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('job')


# Appointment Factory
class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)
    date = factory.LazyFunction(date.today)
    time = factory.LazyFunction(lambda: time(10, 0))  # Default appointment time 10:00 AM
    symptoms = factory.Faker('paragraph')
    ai_summarized_symptoms = factory.Faker('paragraph')
    notes = factory.Faker('paragraph')


# UserActionLog Factory
class UserActionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserActionLog

    user = factory.SubFactory(UserFactory)
    action_type = factory.Faker('word')
    endpoint = factory.Faker('uri')
    ip_address = factory.Faker('ipv4')
    status_code = factory.Faker('random_int', min=200, max=500)
    outcome = factory.Iterator(['Success', 'Failure'])
    details = factory.Faker('sentence')


