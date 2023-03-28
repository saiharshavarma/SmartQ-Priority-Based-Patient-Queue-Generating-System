from django.shortcuts import render, redirect
from .models import Doctor
from accounts.models import Profile
from patient.models import PatientRecord, PatientHistory
import datetime

# Create your views here.
def home(request):
    doctor = Doctor.objects.get(profile=Profile.objects.get(user=request.user))
    records = PatientRecord.objects.filter(appointment_date = datetime.datetime.today(), doctor=doctor).order_by('appointment_time')
    records = list(records)
    context = {
        "records": records,
    }
    return render(request, "doctor/home.html", context)


def appointmentSuccess(request, record):
    record = PatientRecord.objects.get(id=record)
    record.status = True
    record.save()
    patienthistory = PatientHistory.objects.create(patient=record.patient, records=record)
    patienthistory.save()
    return redirect("doctor_home")