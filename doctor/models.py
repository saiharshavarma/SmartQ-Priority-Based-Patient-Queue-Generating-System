from django.db import models
from accounts.models import Profile
import datetime

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
    speciality = models.CharField(max_length = 50, choices=SPECIALITY)
    experience = models.CharField(max_length = 50, choices=EXPERIENCE)

    def __str__(self):
        return str(f'{self.profile}')
    

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today())
    slot_800 = models.BooleanField(default=True)
    slot_830 = models.BooleanField(default=True)
    slot_900 = models.BooleanField(default=True)
    slot_930 = models.BooleanField(default=True)
    slot_1000 = models.BooleanField(default=True)
    slot_1030 = models.BooleanField(default=True)
    slot_1100 = models.BooleanField(default=True)
    slot_1130 = models.BooleanField(default=True)
    slot_1200 = models.BooleanField(default=True)
    slot_1230 = models.BooleanField(default=True)
    slot_1400 = models.BooleanField(default=True)
    slot_1430 = models.BooleanField(default=True)
    slot_1500 = models.BooleanField(default=True)
    slot_1530 = models.BooleanField(default=True)
    slot_1600 = models.BooleanField(default=True)
    slot_1630 = models.BooleanField(default=True)
    slot_1700 = models.BooleanField(default=True)
    slot_1730 = models.BooleanField(default=True)

    def __str__(self):
        return str(f'{self.date}')