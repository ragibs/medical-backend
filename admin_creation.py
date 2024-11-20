# import django
# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
# django.setup()

# from django.contrib.auth.models import User
# from MedAppApi.models import AdminStaff, UserProfile

# admin_staff_data = {
#     "username": "adminstaff",
#     "email": "jarjar.bink@example.com",
#     "password": "securepassword123",
#     "first_name": "JarJar",
#     "last_name": "Binks",
#     "title": "Receptionist"
# }

# def create_admin_staff(data):
#     user = User.objects.create_user(
#         username=data["username"],
#         email=data["email"],
#         password=data["password"],
#         first_name=data["first_name"],
#         last_name=data["last_name"]
#     )

#     user_profile, created = UserProfile.objects.get_or_create(user=user)
#     user_profile.role = 'ADMIN'
#     user_profile.save()

#     AdminStaff.objects.create(
#         user=user,
#         title=data["title"]
#     )

#     print(f"Admin staff {data['first_name']} {data['last_name']} created successfully.")

# create_admin_staff(admin_staff_data)

import django
import os
from django.db import IntegrityError

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
    try:
        # Check if the user already exists
        user = User.objects.get(username=data["username"])
        print(f"User {data['username']} already exists. Skipping creation.")
        return
    except User.DoesNotExist:
        # Create a new user
        try:
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
        except IntegrityError as e:
            print(f"Failed to create user: {e}")
            return

    # Ensure UserProfile exists
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            user_profile.role = 'ADMIN'
            user_profile.save()
    except IntegrityError as e:
        print(f"Failed to create or update UserProfile: {e}")
        return

    # Create AdminStaff record
    try:
        AdminStaff.objects.get_or_create(
            user=user,
            defaults={"title": data["title"]}
        )
        print(f"Admin staff {data['first_name']} {data['last_name']} created successfully.")
    except IntegrityError as e:
        print(f"Failed to create AdminStaff: {e}")

create_admin_staff(admin_staff_data)
