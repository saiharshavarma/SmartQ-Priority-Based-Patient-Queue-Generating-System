from django.contrib import admin
from .models import Doctor, Schedule

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('profile', 'speciality', 'experience')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date')

# Register your models here.
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Schedule, ScheduleAdmin)