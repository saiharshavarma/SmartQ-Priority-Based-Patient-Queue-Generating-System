from django.contrib import admin
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('profile', 'speciality', 'experience')

# Register your models here.
admin.site.register(Doctor, DoctorAdmin)