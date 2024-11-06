import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()


from django.contrib.auth.models import User
from MedAppApi.models import Doctor
specializations = [
    "Cardiology", "Dermatology", "Neurology", "Pediatrics", "Oncology",
    "Orthopedics", "Radiology", "Psychiatry", "Gastroenterology", "Endocrinology"
]

for i, specialization in enumerate(specializations):
    user = User.objects.create_user(
        username=f"doctor{i+1}",
        email=f"doctor{i+1}@example.com",
        password="securepassword123",
        first_name=f"Doctor{i+1}_First",
        last_name=f"Doctor{i+1}_Last"
    )

    Doctor.objects.create(
        user=user,
        phone=f"123-456-78{i+10}",
        specialization=specialization,
        address=f"{i+1} Medical Plaza",
        city="Healthtown",
        state="Wellness",
        zipcode=f"1234{i}",
        bio=f"Experienced in {specialization}.",
        years_experience=i
    )

print("Doctor Creation successful")