from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Sample Models
# class Clinic(models.Model):
#     name = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Look into this for auth can be used for hashed passwords
    # # Not needed if user line is kept
    # created_at = models.DateTimeField(auto_now_add=True)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    bio = models.TextField()
    years_experience = models.IntegerField(null=False)
    # clinic = models.ManyToManyField(Clinic, related_name='doctors')

    # def __str__(self) -> str:
    #     return (f"User ID: {self.user.id} Name:{self.user.first_name} {self.user.last_name}")

class AdminStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    appointments_booked = models.IntegerField(default=0)

    # def __str__(self) -> str:
    #     return (f"User ID: {self.user.id} Name:{self.user.first_name} {self.user.last_name}")

class BasicPatient(Patient):
    maximum_appointments = models.IntegerField(default=100)

class ProPatient(Patient):
    maximum_appointments = models.IntegerField(default=99999999)


class PatientDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    age = models.IntegerField(null=False)
    sex = models.CharField(max_length=15)
    weight = models.IntegerField(validators=[MinValueValidator(0) ,MaxValueValidator(2000)])
    height = models.IntegerField(validators=[MinValueValidator(10) ,MaxValueValidator(500)])
    history = models.TextField()


class Availability():
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    working_days = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom_summary = models.TextField()
    booking_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=60.00)

class Testimonials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testimonial = models.TextField()


class Ratings(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])



# Test table for API delete after
class TestUser(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self) -> str:
        return (f"Name:{self.name} Age:{self.age}")