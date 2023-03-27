from django.shortcuts import render, redirect
from .models import Patient, PatientRecord, PatientHistory
from doctor.models import Doctor
from accounts.models import Profile
from .voicebot import run_bot
import datetime
import re

TIMESLOT = {
    "8:00" : 800,
    "8:30" : 830,
    "9:00" : 900,
    "9:30" : 930,
    "10:00" : 1000,
    "10:30" : 1030,
    "11:00" : 1100,
    "11:30" : 1130,
    "12:00" : 1200,
    "12:30" : 1230,
    "14:00" : 1400,
    "14:30" : 1430,
    "15:00" : 1500,
    "15:30" : 1530,
    "16:00" : 1600,
    "16:30" : 1630,
    "17:00" : 1700,
    "17:30" : 1730,
}

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')


def input(request):
    return render(request, "patient/voicebot.html")


def inputSymptoms(request):
    profile = Profile.objects.get(user=request.user)
    patient = Patient.objects.get(profile=profile)
    symptoms = run_bot(patient.profile)
    speciality = None # fetched from the model based on the symptoms
    severity = assign_criticality(patient.age, patient.gender, patient.past_history, symptoms)
    record = PatientRecord.objects.create(patient=patient, symptoms=symptoms, severity=severity)
    record.save()
    return redirect("check_doctor_availability", record=record)


def fetchPendingAppointments(request):
    appointments = PatientRecord.objects.filter(patient=Patient.objects.get(profile=Profile.objects.get(user=request.user)), status=False)
    print(appointments)
    return render(request, "patient/fetchAppointment.html")


def availableDoctors(request):
    record = PatientRecord.objects.all()[0]
    doctors = Doctor.objects.filter(speciality = record.speciality)
    current_time = datetime.time.now()
    if current_time.minute < 30:
        nearest_half_hour = current_time.replace(minute=30, second=0, microsecond=0)
    else:
        nearest_half_hour = current_time.replace(hour=current_time.hour+1, minute=0, second=0, microsecond=0)
    print(nearest_half_hour)
    available_doctor = None
    bookings_full = True
    for doctor in doctors:
        if nearest_half_hour == "Available":
            available_doctor = doctor
            bookings_full = False
            break
    context = {
        "doctor": available_doctor,
        "time_slot": nearest_half_hour,
        "bookings_full": bookings_full,
    }
    return render(request, "patient/availableDoctors.html", context)


def assign_criticality(age, gender, past_history, current_symptoms):
    score = 0
    
    if int(age) >= 60:
        score += 2
    elif int(age) >= 40:
        score += 1
    
    if gender.lower() == "male":
        score += 1
    
    if "diabetes" in past_history.lower():
        score += 2
    elif "hypertension" in past_history.lower():
        score += 1
    
    if "difficulty breathing" in current_symptoms.lower() or "shortness of breath" in current_symptoms.lower():
        score += 2
    elif "fever" in current_symptoms.lower() or "cough" in current_symptoms.lower() or "sore throat" in current_symptoms.lower():
        score += 1
    
    # Assign criticality score
    if score <= 3:
        return 1
    elif score <= 6:
        return 2
    elif score <= 9:
        return 3
    elif score <= 12:
        return 4
    else:
        return 5