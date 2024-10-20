from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Placeholder
    path('', views.home, name='home'),
    path('testusers/', get_testusers, name='get_testusers'),
    path('testusers/create/', create_testuser, name='create_testuser'),
    path('testusers/<int:pk>', update_testuser, name='update_testuser'),
]