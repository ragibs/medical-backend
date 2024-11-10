import django
import os
import random
from datetime import date, timedelta, time

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

# Import necessary models
from MedAppApi.models import Patient, Doctor, Appointment

# Fetch all existing patients and doctors from the database
patients = list(Patient.objects.all())
doctors = list(Doctor.objects.all())

# Check if we have patients and doctors in the database
if not patients or not doctors:
    print("No patients or doctors available. Please add them first.")
    exit()

# Generate random appointment data
def generate_appointments(num_appointments=20):
    appointments = []
    
    for _ in range(num_appointments):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
        # Generate random date within the next 30 days
        appointment_date = date.today() + timedelta(days=random.randint(1, 30))
        # Generate random time for the appointment between 9 AM to 5 PM
        appointment_time = time(hour=random.randint(9, 16), minute=random.choice([0, 30]))

        # Set fixed data for symptoms, AI summary, and notes
        symptoms = "Patient reports mild headache and fatigue."
        ai_summary = "AI-generated summary: Possible tension headache."
        notes = "Follow-up needed if symptoms persist."

        # Create an Appointment object
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            date=appointment_date,
            time=appointment_time,
            symptoms=symptoms,
            ai_summarized_symptoms=ai_summary,
            notes=notes
        )
        appointments.append(appointment)

    return appointments

# Generate and save the appointments
appointments = generate_appointments(num_appointments=30)
Appointment.objects.bulk_create(appointments)

print("Appointments created successfully.")