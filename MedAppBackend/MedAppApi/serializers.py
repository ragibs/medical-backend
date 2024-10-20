# Info https://www.django-rest-framework.org/tutorial/quickstart/

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *

# serializers.HyperlinkedModelSerializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestUser
        fields = '__all__'