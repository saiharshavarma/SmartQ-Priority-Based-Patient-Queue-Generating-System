from django.db import models
from accounts.models import Profile
from doctor.models import Doctor

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)

SEVERITY = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)

class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    patient_id = models.IntegerField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length = 50, choices=GENDER)


class PatientRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField()
    severity = models.IntegerField(choices=SEVERITY)


class PatientHistory(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    records = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)