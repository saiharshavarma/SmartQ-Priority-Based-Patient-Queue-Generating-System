from django.db import models
from accounts.models import Profile

SPECIALITY = (
    ("Orthopedics", "Orthopedics"),
    ("Obstetrics and Gynecology", "Obstetrics and Gynecology"),
    ("Dermatology", "Dermatology"),
    ("Pediatrics", "Pediatrics"),
    ("General Surgery", "General Surgery"),
    ("Ophthalmology", "Ophthalmology"),
    ("Neurology", "Neurology"),
    ("Cardiology", "Cardiology"),
    ("Nephrology", "Nephrology"),
    ("Oncology", "Oncology"),
    )

EXPERIENCE = (
    ("Attending", "Attending"),
    ("3rd year Resident", "3rd year Resident"),
    ("2nd year Resident", "2nd year Resident"),
    ("1st year Resident", "1st year Resident"),
    )

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    employee_id = models.IntegerField(unique=True)
    speciality = models.CharField(choices=SPECIALITY)
    experience = models.CharField(choices=EXPERIENCE)
