import django
import os
from django.contrib.auth.models import User
from MedAppApi.models import UserProfile, AdminStaff

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MedAppBackend.settings")
django.setup()

# Example admin data
admin_data = {
    "username": "admin_user",
    "email": "admin@example.com",
    "password": "adminpassword123",
    "first_name": "Admin",
    "last_name": "User",
    "title": "Administrator"
}

# Check if admin exists
if not User.objects.filter(username=admin_data["username"]).exists():
    # Create the User instance for the admin
    admin_user = User.objects.create_superuser(
        username=admin_data["username"],
        email=admin_data["email"],
        password=admin_data["password"],
        first_name=admin_data["first_name"],
        last_name=admin_data["last_name"]
    )

    # Step 2: Create the UserProfile instance and set role to "ADMIN"
    UserProfile.objects.create(user=admin_user, role='ADMIN')

    # Step 3: Create the AdminStaff instance and assign a title
    AdminStaff.objects.create(user=admin_user, title=admin_data["title"])

    print("Admin user created successfully.")
else:
    print("Admin user already exists.")