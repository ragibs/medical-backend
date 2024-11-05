from django.urls import path
from dj_rest_auth.views import LoginView
from . import views
from .views import *

urlpatterns = [
    # Placeholder
    path('', views.home, name='home'),
    path('testusers/', get_testusers, name='get_testusers'),
    path('testusers/create/', create_testuser, name='create_testuser'),
    path('testusers/<int:pk>', update_testuser, name='update_testuser'),
    path('login', LoginView.as_view(), name='login'),
    path('api/register_patient/', register_patient, name='register_patient'),
]