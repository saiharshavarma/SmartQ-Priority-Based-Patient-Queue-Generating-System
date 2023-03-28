from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name="patient_home"),
    path('myappointments', views.fetchPendingAppointments, name="appointment_details"),
    #path('available_doctors/<record>', views.availableDoctors, name="check_doctor_availability"),
    path('available_doctors/', views.availableDoctors, name="check_doctor_availability"),
    path('input/', views.input, name="input"),
    path('inputSymptoms/', views.inputSymptoms, name="input"),
    path('confirm_bookings/<doctor>/<slot>/<time>', views.confirmBooking, name="confirm_bookings")
]
