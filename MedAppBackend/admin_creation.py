import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

from django.contrib.auth.models import User
from MedAppApi.models import AdminStaff, UserProfile

admin_staff_data = {
    "username": "adminstaff",
    "email": "jarjar.bink@example.com",
    "password": "securepassword123",
    "first_name": "JarJar",
    "last_name": "Binks",
    "title": "Receptionist"
}

def create_admin_staff(data):
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        first_name=data["first_name"],
        last_name=data["last_name"]
    )

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.role = 'ADMIN'
    user_profile.save()

    AdminStaff.objects.create(
        user=user,
        title=data["title"]
    )

    print(f"Admin staff {data['first_name']} {data['last_name']} created successfully.")

create_admin_staff(admin_staff_data)