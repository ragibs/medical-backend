import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

from django.db.utils import IntegrityError # Added
from django.contrib.auth.models import User
from MedAppApi.models import Doctor, UserProfile

# List of fake doctors  
doctors = [
    {
        "username": "dr_johnsmith",
        "email": "johnsmith@example.com",
        "password": "securepassword123",
        "first_name": "John",
        "last_name": "Smith",
        "phone": "213-555-1010", 
        "specialization": "Cardiology",
        "address": "123 Heartbeat Lane",
        "city": "Los Angeles",
        "state": "CA",
        "zipcode": "90001",
        "bio": "Dr. John Smith has over 15 years of experience in cardiology. Previously worked at Cedars-Sinai Medical Center and specializes in treating heart conditions and performing complex surgeries.",
        "short_bio": "Cardiologist with 15 years experience",
        "years_experience": 15
    },
    {
        "username": "dr_liwang",
        "email": "liwang@example.com",
        "password": "securepassword123",
        "first_name": "Li",
        "last_name": "Wang",
        "phone": "646-555-2020",  
        "specialization": "Dermatology",
        "address": "456 SkinCare Ave",
        "city": "New York",
        "state": "NY",
        "zipcode": "10001",
        "bio": "Dr. Li Wang is a board-certified dermatologist with 10 years of experience. She previously practiced at Mount Sinai Hospital and specializes in skin conditions, including acne, eczema, and skin cancer.",
        "short_bio": "Dermatologist with 10 years experience",
        "years_experience": 10
    },
    {
        "username": "dr_michaeltaylor",
        "email": "michaeltaylor@example.com",
        "password": "securepassword123",
        "first_name": "Michael",
        "last_name": "Taylor",
        "phone": "312-555-3030",  
        "specialization": "Pediatrics",
        "address": "789 Kids Health St",
        "city": "Chicago",
        "state": "IL",
        "zipcode": "60601",
        "bio": "Dr. Michael Taylor has been a pediatrician for 12 years. He has worked at Chicago Children's Hospital, specializing in child health and development, providing care from infancy through adolescence.",
        "short_bio": "Pediatrician with 12 years experience",
        "years_experience": 12
    },
    {
        "username": "dr_emilygarcia",
        "email": "emilygarcia@example.com",
        "password": "securepassword123",
        "first_name": "Emily",
        "last_name": "Garcia",
        "phone": "713-555-4040",  
        "specialization": "Orthopedics",
        "address": "234 BoneCare Blvd",
        "city": "Houston",
        "state": "TX",
        "zipcode": "77002",
        "bio": "Dr. Emily Garcia is an orthopedic surgeon with 8 years of experience, specializing in sports injuries and joint replacements. She has worked at Houston General Hospital.",
        "short_bio": "Orthopedic surgeon with 8 years experience",
        "years_experience": 8
    },
    {
        "username": "dr_davidbrown",
        "email": "davidbrown@example.com",
        "password": "securepassword123",
        "first_name": "David",
        "last_name": "Brown",
        "phone": "602-555-5050",  
        "specialization": "Neurology",
        "address": "567 Brain Health Rd",
        "city": "Phoenix",
        "state": "AZ",
        "zipcode": "85001",
        "bio": "Dr. David Brown is a neurologist with 14 years of experience. He specializes in treating neurological disorders, including epilepsy and Parkinson's, and previously worked at Arizona Neurology Institute.",
        "short_bio": "Neurologist with 14 years experience",
        "years_experience": 14
    },
    {
        "username": "dr_sarahabdi",
        "email": "sarahabdi@example.com",
        "password": "securepassword123",
        "first_name": "Sarah",
        "last_name": "Abdi",
        "phone": "415-555-6060",  
        "specialization": "Ophthalmology",
        "address": "890 Vision Lane",
        "city": "San Francisco",
        "state": "CA",
        "zipcode": "94102",
        "bio": "Dr. Sarah Abdi is an ophthalmologist with over 9 years of experience in eye care. She has worked at San Francisco Eye Center, treating conditions like cataracts and glaucoma.",
        "short_bio": "Ophthalmologist with 9 years experience",
        "years_experience": 9
    },
    {
        "username": "dr_ameenkhan",
        "email": "ameenkhan@example.com",
        "password": "securepassword123",
        "first_name": "Ameen",
        "last_name": "Khan",
        "phone": "206-555-7070",  
        "specialization": "Psychiatry",
        "address": "123 Mind St",
        "city": "Seattle",
        "state": "WA",
        "zipcode": "98101",
        "bio": "Dr. Ameen Khan is a psychiatrist with 11 years of experience, specializing in mental health conditions like anxiety and depression. He previously worked at Seattle Mental Health Clinic.",
        "short_bio": "Psychiatrist with 11 years experience",
        "years_experience": 11
    },
    {
        "username": "dr_mariamlopez",
        "email": "mariamlopez@example.com",
        "password": "securepassword123",
        "first_name": "Mariam",
        "last_name": "Lopez",
        "phone": "305-555-8080",  
        "specialization": "Gastroenterology",
        "address": "456 Digestive Way",
        "city": "Miami",
        "state": "FL",
        "zipcode": "33101",
        "bio": "Dr. Mariam Lopez is a gastroenterologist with 10 years of experience, specializing in digestive health and conditions like IBS and Crohn's disease. Previously worked at Miami Gastroenterology Center.",
        "short_bio": "Gastroenterologist with 10 years experience",
        "years_experience": 10
    },
    {
        "username": "dr_kofianderson",
        "email": "kofianderson@example.com",
        "password": "securepassword123",
        "first_name": "Kofi",
        "last_name": "Anderson",
        "phone": "404-555-9090",  
        "specialization": "Oncology",
        "address": "789 Cancer Care St",
        "city": "Atlanta",
        "state": "GA",
        "zipcode": "30301",
        "bio": "Dr. Kofi Anderson is an oncologist with 13 years of experience. He specializes in cancer treatment, including chemotherapy and immunotherapy, and has worked at Emory Cancer Institute.",
        "short_bio": "Oncologist with 13 years experience",
        "years_experience": 13
    },
    {
        "username": "dr_karennguyen",
        "email": "karenguyen@example.com",
        "password": "securepassword123",
        "first_name": "Karen",
        "last_name": "Nguyen",
        "phone": "617-555-1111",  
        "specialization": "Endocrinology",
        "address": "321 Hormone Ave",
        "city": "Boston",
        "state": "MA",
        "zipcode": "02108",
        "bio": "Dr. Karen Nguyen is an endocrinologist with 7 years of experience, focusing on hormone-related conditions like diabetes and thyroid disorders. She previously worked at Massachusetts Endocrine Center.",
        "short_bio": "Endocrinologist with 7 years experience",
        "years_experience": 7
    },
    {
    "username": "dr_alexmartin",
    "email": "alexmartin@example.com",
    "password": "securepassword123",
    "first_name": "Alex",
    "last_name": "Martin",
    "phone": "212-555-2222",
    "specialization": "General Practice",
    "address": "555 Health Blvd",
    "city": "New York",
    "state": "NY",
    "zipcode": "10011",
    "bio": "Dr. Alex Martin is a General Practitioner with 10 years of experience in providing comprehensive primary care. He is skilled in diagnosing and managing a wide range of conditions and is dedicated to preventive healthcare.",
    "short_bio": "General Practitioner with 10 years experience",
    "years_experience": 10
    }
]

# for doctor_data in doctors:
#     # Step 1: Create the User instance
#     user = User.objects.create_user(
#         username=doctor_data["username"],
#         email=doctor_data["email"],
#         password=doctor_data["password"],
#         first_name=doctor_data["first_name"],
#         last_name=doctor_data["last_name"]
#     )

#     # Step 2: Create the UserProfile instance and set role to "DOCTOR"
#     UserProfile.objects.create(user=user, role='DOCTOR')

#     # Step 3: Create the Doctor instance
#     Doctor.objects.create(
#         user=user,
#         phone=doctor_data["phone"],
#         specialization=doctor_data["specialization"],
#         address=doctor_data["address"],
#         city=doctor_data["city"],
#         state=doctor_data["state"],
#         zipcode=doctor_data["zipcode"],
#         bio=doctor_data["bio"],
#         short_bio=doctor_data["short_bio"],
#         years_experience=doctor_data["years_experience"]
#     )

# print("Doctor Creation successful")

for doctor_data in doctors:
    try:
        # Step 1: Check if User already exists to avoid IntegrityError
        if not User.objects.filter(username=doctor_data["username"]).exists():

            # Step 1: Create the User instance
            user = User.objects.create_user(
                username=doctor_data["username"],
                email=doctor_data["email"],
                password=doctor_data["password"],
                first_name=doctor_data["first_name"],
                last_name=doctor_data["last_name"]
            )

            # Step 2: Create the UserProfile instance and set role to "DOCTOR"
            UserProfile.objects.create(user=user, role='DOCTOR')

            # Step 3: Create the Doctor instance
            Doctor.objects.create(
                user=user,
                phone=doctor_data["phone"],
                specialization=doctor_data["specialization"],
                address=doctor_data["address"],
                city=doctor_data["city"],
                state=doctor_data["state"],
                zipcode=doctor_data["zipcode"],
                bio=doctor_data["bio"],
                short_bio=doctor_data["short_bio"],
                years_experience=doctor_data["years_experience"]
            )
            print(f"Doctor {doctor_data['username']} created successfully.")
        else:
            print(f"Doctor {doctor_data['username']} already exists. Skipping creation.")

    except IntegrityError as e:
        print(f"IntegrityError occurred for {doctor_data['username']}: {e}")

print("Doctor creation process completed.")