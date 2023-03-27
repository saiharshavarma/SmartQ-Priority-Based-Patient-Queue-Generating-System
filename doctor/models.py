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

TIMESLOT = (
    (800, "8:00  - 8:30"),
    (830, "8:30  - 9:00"),
    (900, "9:00  - 9:30"),
    (930, "9:30  - 10:00"),
    (1000, "10:00 - 10:30"),
    (1030, "10:30 - 11:00"),
    (1100, "11:00 - 11:30"),
    (1130, "11:30 - 12:00"),
    (1200, "12:00 - 12:30"),
    (1230, "12:30 - 13:00"),
    (1400, "14:00 - 14:30"),
    (1430, "14:30 - 15:00"),
    (1500, "15:00 - 15:30"),
    (1530, "15:30 - 16:00"),
    (1600, "16:00 - 16:30"),
    (1630, "16:30 - 17:00"),
    (1700, "17:00 - 17:30"),
    (1730, "17:30 - 18:00"),
)

class Schedule(models.Model):
    date = models.DateField(default=datetime.date.today())
    timeslot = models.IntegerField(choices=TIMESLOT)

    def __str__(self):
        return str(self.date)

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    speciality = models.CharField(max_length = 50, choices=SPECIALITY)
    experience = models.CharField(max_length = 50, choices=EXPERIENCE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.profile}')