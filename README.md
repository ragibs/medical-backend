

### MediCal Application

### Overview

MediCal is a comprehensive healthcare management system designed to streamline patient, doctor, and administrative workflows.It is a user friendly appointment app that allows patients to book appointments with Doctors in just a few clicks. Patients and Doctors can come together on the same platform. Patients can easily book and manage their appointments as well as view their appointment records. The application includes both backend and frontend components developed using Django and React, respectively. 


### Features
**User Profile Management**: Manage user profiles including patients, doctors, and admin staff.

**Patient, Doctor, and AdminStaff Registration**: Register different user roles with appropriate details.

**Appointment Scheduling**: Schedule, validate, and manage appointments between patients and doctors.

**Logging**: Track user actions and log them for auditing purposes.

**Custom Login and Access Permissions**: Secure login and role-based access control.




#### Frontend Technologies
See GitHub Repo :https://github.com/ragibs/medical-frontend.git

#### Backend Technologies
Django

Pytest (for testing)

Factory Boy (for test data generation)


### Installation
Prerequisites
Python 3.x

### Project Setup 

#### Backend Setup
To set up the project locally, follow these steps:

**Step 1: Clone the repository**

```bash
git clone https://github.com/ragibs/medical-backend.git
cd medical-backend
```

**Step 2: Create a Virtual Environment**
```bash
python -m venv Virtual
```

**Step 3: Activate Virtual Environment on Windows**

```bash
source Virtual/Scripts/activate
```

**Step 4: Install Required Packages**

```bash
pip install -r requirements.txt
```

**Step 5: Navigate to Backend Directory**

```bash
cd MedAppBackend/
```
**Step 6: Create the Database (Run Only Once)**

Make sure to create a .env file with your information first. You can place it in the Virtual folder.

```bash
python dbcreation.py
```

**Step 7: Make Migrations**

```bash
python manage.py makemigrations
```

**Step 7: Apply Migrations**

```bash
python manage.py migrate
```

**Step 9: Create Doctor Data (Optional - to create some doctor data in the database)**

```bash
python doctor_creation.py
```

**Step 10: Create Patient Data (Optional - to create some patient date in the database)**

```bash
python patient_creation.py
```

**Step 11: Create Admin Data (Optional - to create some admin data in the database)**

```bash
python admin_creation.py
```

**Step 12: Run the Server (Port 8000 is Optional Since It’s Specified in settings.py)**

```bash
python manage.py runserver 8000
```
### Frontend Setup
See link: https://github.com/ragibs/medical-frontend.git

### Running Tests
##### Backend Tests
To run the backend tests, use Pytest:

```bash
cd MedAppApi
pytest
```



### Acknowledgements
Django

React

Pytest

Factory Boy

Jest

React Testing Library

