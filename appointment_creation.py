import django
import os
import random
from datetime import datetime, date, timedelta, time

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

from MedAppApi.models import Patient, Doctor, Appointment

# Fetch all existing patients and doctors from the database
patients = list(Patient.objects.all())
doctors = list(Doctor.objects.all())

# Check if we have patients and doctors in the database
if not patients or not doctors:
    print("No patients or doctors available. Please add them first.")
    exit()

# List of varied symptoms and AI summaries
symptoms_list = [
    ("Cough, fever, and fatigue", "AI-generated summary: Possible viral infection."),
    ("Severe headache and blurred vision", "AI-generated summary: Possible migraine."),
    ("Joint pain and stiffness", "AI-generated summary: Possible arthritis flare-up."),
    ("Stomach pain and nausea", "AI-generated summary: Possible gastritis."),
    ("Shortness of breath and chest tightness", "AI-generated summary: Possible asthma attack."),
    ("Frequent urination and excessive thirst", "AI-generated summary: Possible diabetes."),
    ("Lower back pain and muscle spasms", "AI-generated summary: Possible muscle strain."),
    ("Skin rash and itching", "AI-generated summary: Possible allergic reaction."),
    ("Sore throat and difficulty swallowing", "AI-generated summary: Possible strep throat."),
    ("Ear pain and dizziness", "AI-generated summary: Possible ear infection."),
    ("Abdominal cramps and diarrhea", "AI-generated summary: Possible food poisoning."),
    ("Fatigue and pale skin", "AI-generated summary: Possible anemia."),
    ("Chest pain and palpitations", "AI-generated summary: Possible heart arrhythmia."),
    ("Swelling in legs and feet", "AI-generated summary: Possible fluid retention."),
    ("Fever and body aches", "AI-generated summary: Possible flu."),
    ("Painful urination", "AI-generated summary: Possible urinary tract infection."),
    ("Difficulty breathing while sleeping", "AI-generated summary: Possible sleep apnea."),
    ("Persistent cough with mucus", "AI-generated summary: Possible bronchitis."),
    ("Numbness in hands and feet", "AI-generated summary: Possible peripheral neuropathy."),
    ("Sudden weight loss", "AI-generated summary: Possible thyroid disorder.")
]

# Function to generate appointments within the specified date range
def generate_appointments(num_appointments=20):
    appointments = []
    start_date = datetime(2024, 11, 20)
    end_date = datetime(2024, 12, 5)

    for _ in range(num_appointments):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
        # Generate random date between November 20th and December 5th
        appointment_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        # Generate random time between 9 AM to 5 PM
        appointment_time = time(hour=random.randint(9, 16), minute=random.choice([0, 30]))

        # Randomly select symptoms and AI summary
        symptoms, ai_summary = random.choice(symptoms_list)

        # Create an Appointment object
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            date=appointment_date,
            time=appointment_time,
            symptoms=symptoms,
            ai_summarized_symptoms=ai_summary,
            notes="Follow-up needed if symptoms persist."
        )
        appointments.append(appointment)

    return appointments

# Generate and save the appointments
appointments = generate_appointments(num_appointments=20)
Appointment.objects.bulk_create(appointments)

print("Appointments created successfully.")