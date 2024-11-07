import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

from django.contrib.auth.models import User
from MedAppApi.models import Patient, UserProfile

# List of patient data
patients = [
    {
        "username": "patient_mariahernandez",
        "email": "mariahernandez@example.com",
        "password": "securepassword123",
        "first_name": "Maria",
        "last_name": "Hernandez",
        "phone": "213-555-1010",  
        "address": "123 Maple St",
        "city": "Los Angeles",
        "state": "CA",
        "zipcode": "90001",
        "date_of_birth": "1990-05-14"
    },
    {
        "username": "patient_chenli",
        "email": "chenli@example.com",
        "password": "securepassword123",
        "first_name": "Chen",
        "last_name": "Li",
        "phone": "415-555-2020",  
        "address": "456 Oak Rd",
        "city": "San Francisco",
        "state": "CA",
        "zipcode": "94103",
        "date_of_birth": "1985-08-22"
    },
    {
        "username": "patient_johnsmith",
        "email": "johnsmith@example.com",
        "password": "securepassword123",
        "first_name": "John",
        "last_name": "Smith",
        "phone": "646-555-3030",  
        "address": "789 Pine Ave",
        "city": "New York",
        "state": "NY",
        "zipcode": "10001",
        "date_of_birth": "1978-11-05"
    },
    {
        "username": "patient_ayeshakhan",
        "email": "ayeshakhan@example.com",
        "password": "securepassword123",
        "first_name": "Ayesha",
        "last_name": "Khan",
        "phone": "713-555-4040", 
        "address": "321 Cedar Ln",
        "city": "Houston",
        "state": "TX",
        "zipcode": "77002",
        "date_of_birth": "1992-04-19"
    },
    {
        "username": "patient_davidsmith",
        "email": "davidsmith@example.com",
        "password": "securepassword123",
        "first_name": "David",
        "last_name": "Smith",
        "phone": "312-555-5050",  
        "address": "654 Elm St",
        "city": "Chicago",
        "state": "IL",
        "zipcode": "60616",
        "date_of_birth": "1980-09-25"
    },
    {
        "username": "patient_ruthnjeri",
        "email": "ruthnjeri@example.com",
        "password": "securepassword123",
        "first_name": "Ruth",
        "last_name": "Njeri",
        "phone": "404-555-6060",  
        "address": "432 Birch Blvd",
        "city": "Atlanta",
        "state": "GA",
        "zipcode": "30303",
        "date_of_birth": "1988-07-12"
    },
    {
        "username": "patient_olivernguyen",
        "email": "olivernguyen@example.com",
        "password": "securepassword123",
        "first_name": "Oliver",
        "last_name": "Nguyen",
        "phone": "206-555-7070",  
        "address": "567 Walnut St",
        "city": "Seattle",
        "state": "WA",
        "zipcode": "98101",
        "date_of_birth": "1995-02-03"
    },
    {
        "username": "patient_luciaferrari",
        "email": "luciaferrari@example.com",
        "password": "securepassword123",
        "first_name": "Lucia",
        "last_name": "Ferrari",
        "phone": "305-555-8080",  
        "address": "678 Spruce Rd",
        "city": "Miami",
        "state": "FL",
        "zipcode": "33101",
        "date_of_birth": "1993-12-17"
    },
    {
        "username": "patient_mohamedali",
        "email": "mohamedali@example.com",
        "password": "securepassword123",
        "first_name": "Mohamed",
        "last_name": "Ali",
        "phone": "214-555-9090",  
        "address": "987 Palm Ave",
        "city": "Dallas",
        "state": "TX",
        "zipcode": "75201",
        "date_of_birth": "1982-10-10"
    },
    {
        "username": "patient_nataliewong",
        "email": "nataliewong@example.com",
        "password": "securepassword123",
        "first_name": "Natalie",
        "last_name": "Wong",
        "phone": "617-555-1111",  
        "address": "1010 Willow Ct",
        "city": "Boston",
        "state": "MA",
        "zipcode": "02108",
        "date_of_birth": "1997-06-25"
    }
]

# Loop through the list of patients and create User and Patient records
for patient_data in patients:
    user = User.objects.create_user(
        username=patient_data["username"],
        email=patient_data["email"],
        password=patient_data["password"],
        first_name=patient_data["first_name"],
        last_name=patient_data["last_name"]
    )

    UserProfile.objects.create(user=user, role='PATIENT')


    Patient.objects.create(
        user=user,
        phone=patient_data["phone"],
        address=patient_data["address"],
        city=patient_data["city"],
        state=patient_data["state"],
        zipcode=patient_data["zipcode"],
        date_of_birth=patient_data["date_of_birth"]
    )

print("Patient Creation successful")