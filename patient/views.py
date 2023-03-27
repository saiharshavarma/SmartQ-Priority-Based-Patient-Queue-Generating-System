from django.shortcuts import render
from .models import Patient, PatientRecord, PatientHistory
from accounts.models import Profile

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')

def fetchPendingAppointments(request):
    appointment = PatientRecord.objects.filter(patient=Patient.objects.get(profile=Profile.objects.get(user=request.user)), status=False)
    print(appointment)
    return render(request, "patient/fetchAppointment.html")
