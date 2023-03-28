from django.db import models
from accounts.models import Profile
from doctor.models import Doctor, SPECIALITY

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)

SEVERITY = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

PAST_HISTORY = (
    ("Diabetes", "Diabetes"),
    ("Hypertension", "Hypertension"),
    ("None", "None"),
)

class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length = 50, choices=GENDER)
    past_history = models.CharField(max_length = 50, choices=PAST_HISTORY, default="None")

    def __str__(self):
        return str(f'{self.profile}')


class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    symptoms = models.TextField()
    severity = models.IntegerField(choices=SEVERITY)
    speciality = models.CharField(max_length = 50, choices=SPECIALITY, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(f'{self.pk}' + ' ' + f'{self.patient.profile}')


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    records = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)