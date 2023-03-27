from django.contrib import admin
from .models import Patient, PatientRecord, PatientHistory

class PatientAdmin(admin.ModelAdmin):
    list_display = ('profile', 'age', 'gender')

class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')

class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'records')

# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientRecord, PatientRecordAdmin)
admin.site.register(PatientHistory, PatientHistoryAdmin)