from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name="doctor_home"),
    path('appointment_complete/<record>', views.appointmentSuccess, name="doctor_home"),
]
