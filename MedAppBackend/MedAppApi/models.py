from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

# User Profile Model, assign roles based on sign up
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    date_of_birth = models.DateField()

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    bio = models.TextField()
    short_bio = models.CharField(max_length=150, default="Experienced professional") 
    years_experience = models.IntegerField(null=False)

class AdminStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()  # Date of the appointment
    time = models.TimeField()  # Time of the appointment
    symptoms = models.TextField()  # Description of symptoms
    ai_summarized_symptoms = models.TextField(blank=True, null=True)  # AI summarized symptoms
    notes = models.TextField(blank=True, null=True)  # Notes added by doctor (optional)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

