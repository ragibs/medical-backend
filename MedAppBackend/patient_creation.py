import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()


from django.contrib.auth.models import User
from MedAppApi.models import Patient
names = [
    ("John", "Doe"),
    ("Jane", "Smith"),
    ("Michael", "Johnson"),
    ("Emily", "Davis"),
    ("David", "Brown"),
    ("Olivia", "Williams"),
    ("James", "Taylor"),
    ("Sophia", "Miller"),
    ("Matthew", "Wilson"),
    ("Isabella", "Moore")
]


for i, names in enumerate(names):
    user = User.objects.create_user(
        username=f"patient{i+1}",
        email=f"patient{i+1}@example.com",
        password="securepassword123",
        first_name=f"{names[0]}",
        last_name=f"{names[1]}"
    )

    Patient.objects.create(
        user=user,
        phone=f"123-456-78{i+10}",
        address=f"{i+1} Patient Plaza",
        city="Healthtown",
        state="Wellness",
        zipcode=f"1234{i}",
        appointments_booked=0
    )

print("Patient Creation successful")