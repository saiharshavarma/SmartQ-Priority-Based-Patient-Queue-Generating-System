from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor
from accounts.models import Profile
from patient.models import PatientRecord, PatientHistory
import datetime

# Create your views here.
@login_required(login_url='login')
def home(request):
    doctor = Doctor.objects.get(profile=Profile.objects.get(user=request.user))
    records = PatientRecord.objects.filter(appointment_date = datetime.datetime.today(), doctor=doctor).order_by('appointment_time')
    records = list(records)
    context = {
        "doctor": doctor,
        "records": records,
        "date": datetime.date.today(),
    }
    return render(request, "doctor/home.html", context)


@login_required(login_url='login')
def appointmentSuccess(request, record):
    record = PatientRecord.objects.get(id=record)
    record.status = True
    record.save()
    patienthistory = PatientHistory.objects.create(patient=record.patient, records=record)
    patienthistory.save()
    return redirect("doctor_home")