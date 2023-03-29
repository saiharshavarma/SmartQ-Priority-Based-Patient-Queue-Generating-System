from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, PatientRecord, PatientHistory
from doctor.models import Doctor, Schedule
from accounts.models import Profile
from .voicebot import run_bot
from .speciality import medDepart
import datetime
import re
import pickle

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')


@login_required(login_url='login')
def input(request):
    return render(request, "patient/voicebot.html")


@login_required(login_url='login')
def inputSymptoms(request):
    profile = Profile.objects.get(user=request.user)
    patient = Patient.objects.get(profile=profile)
    symptoms = run_bot(patient.profile)
    speciality = medDepart(symptoms) # fetched from the model based on the symptoms

    if "fever" in symptoms:
        fever = 'Yes'
    else:
        fever = 'No'
    if "cough" in symptoms:
        cough = 'Yes'
    else:
        cough = 'No'
    if "sore throat" in symptoms:
        sore_throat = 'Yes'
    else:
        sore_throat = 'No'
    if "difficulty breathing" in symptoms:
        difficulty_breathing = 'Yes'
    else:
        difficulty_breathing = 'No'
    if "shortness of breath" in symptoms:
        shortness_of_breath = 'Yes'
    else:
        shortness_of_breath = 'No'
    if "diabetes" in symptoms:
        diabetes_history = 'Yes'
    else:
        diabetes_history = 'No'
    if "hypertension" in symptoms:
        hypertension_history = 'Yes'
    else:
        hypertension_history = 'No'

    severity = predictCriticality(patient.age, patient.gender, diabetes_history, hypertension_history, fever, cough, sore_throat, difficulty_breathing, shortness_of_breath)
    record = PatientRecord.objects.create(patient=patient, symptoms=symptoms, speciality=speciality, severity=5)
    record.save()
    return redirect("check_doctor_availability", record=record.id)


@login_required(login_url='login')
def fetchPendingAppointments(request):
    appointments = PatientRecord.objects.filter(patient=Patient.objects.get(profile=Profile.objects.get(user=request.user)), status=False)
    print(appointments)
    return render(request, "patient/fetchAppointment.html")


@login_required(login_url='login')
def availableDoctors(request, record):
    record = PatientRecord.objects.filter(id=record, patient=Patient.objects.get(profile=Profile.objects.get(user=request.user)))[0]
    doctors = Doctor.objects.filter(speciality = record.speciality)
    current_time = datetime.datetime.now()
    if current_time.minute < 30:
        nearest_half_hour = current_time.replace(minute=30, second=0, microsecond=0)
    else:
        nearest_half_hour = current_time.replace(hour=current_time.hour+1, minute=0, second=0, microsecond=0)
    
    print(nearest_half_hour)

    if nearest_half_hour.hour < 8:
        nearest_half_hour = nearest_half_hour.replace(hour=8, minute=0, second=0, microsecond=0)

    available_doctor = None
    bookings_full = True
    slot_check = nearest_half_hour
    slot_check_str = str(slot_check).split(" ")[-1][:5]
    slot = None
    rescheduling = False
    if record.severity == 5:
        for doctor in doctors:
            schedule = Schedule.objects.get_or_create(date=datetime.date.today(), doctor=doctor)
            schedule = Schedule.objects.get(date=datetime.date.today(), doctor=doctor)
            slot_check_str = str(slot_check).split(" ")[-1][:5]
            slot = fetchNearestTimeSlot(schedule, slot_check_str)
            if slot != None:
                available_doctor = doctor
                bookings_full = False
                break
        if bookings_full == True:
            available_doctor = doctors[0]
            slot_check_str = str(slot_check).split(" ")[-1][:5]
            slot = fetchNearestTimeSlot(schedule, slot_check_str)
            rescheduling = True
    else:
        while int(slot_check_str.split(":")[0]) < 18:
            print(slot_check_str)
            for doctor in doctors:
                schedule = Schedule.objects.get_or_create(date=datetime.date.today(), doctor=doctor)
                schedule = Schedule.objects.get(date=datetime.date.today(), doctor=doctor)
                slot_check_str = str(slot_check).split(" ")[-1][:5]
                slot = fetchNearestTimeSlot(schedule, slot_check_str)
                print("Slot: ", slot)
                if slot != None:
                    available_doctor = doctor
                    bookings_full = False
                    break
            if available_doctor != None:
                break
            else:
                if slot_check.minute == 30:
                    slot_check = slot_check.replace(hour=slot_check.hour+1, minute=0, second=0, microsecond=0)
                else:
                    slot_check = slot_check.replace(minute=30, second=0, microsecond=0)
            slot_check_str = str(slot_check).split(" ")[-1][:5]
        if bookings_full == True:
            print("No slots available for today")
    context = {
        "doctor": available_doctor,
        "time_slot": slot,
        "bookings_full": bookings_full,
        "time": slot_check_str,
        "resheduling": rescheduling,
        "date": datetime.date.today(),
    }
    # return redirect("confirm_bookings", doctor=available_doctor.id, slot=slot, time=slot_check)
    return render(request, "patient/availableDoctors.html", context)


@login_required(login_url='login')
def confirmBooking(request, doctor, slot, time, rescheduling):
    schedule = Schedule.objects.get(date=datetime.date.today(), doctor=doctor)
    record = list(PatientRecord.objects.filter(patient=Patient.objects.get(profile=Profile.objects.get(user=request.user))))[0]
    doctor = Doctor.objects.get(id=doctor)

    if rescheduling == "True":
        records = PatientRecord.objects.filter(appointment_date = datetime.datetime.today(), doctor=doctor).order_by('appointment_time')
        records = list(records)
        print(records)
        filtered_records = []
        for precord in records:
            print("Precord: ", precord)
            if datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%S") >= datetime.datetime.strptime(time, "%H:%M"):
                filtered_records.append(precord)
        clashing = True
        print("filtered_records", filtered_records)
        counter = 0
        while counter < len(filtered_records) and clashing:
            precord = filtered_records[counter]
            if precord.appointment_time.minute == 30:
                precord.appointment_time = precord.appointment_time.replace(hour=precord.appointment_time.hour+1, minute=0, second=0, microsecond=0)
            else:
                precord.appointment_time = precord.appointment_time.replace(hour=precord.appointment_time.hour, minute=30, second=0, microsecond=0)
            precord.save()
            try:
                nextrecord = filtered_records[counter+1]
            except:
                nextrecord = filtered_records[0]
                nextrecord.appointment_time = None
            if precord.appointment_time == nextrecord.appointment_time:
                clashing = True
            else:
                clashing = False
            if clashing == False:
                if datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("08:00", "%H:%M"):
                    schedule.slot_800 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("08:30", "%H:%M"):
                    schedule.slot_830 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("09:00", "%H:%M"):
                    schedule.slot_900 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("09:30", "%H:%M"):
                    schedule.slot_930 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("10:00", "%H:%M"):
                    schedule.slot_1000 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("10:30", "%H:%M"):
                    schedule.slot_1030 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("11:00", "%H:%M"):
                    schedule.slot_1100 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("11:30", "%H:%M"):
                    schedule.slot_1130 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("12:00", "%H:%M"):
                    schedule.slot_1200 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("12:30", "%H:%M"):
                    schedule.slot_1230 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("14:00", "%H:%M"):
                    schedule.slot_1400 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("14:30", "%H:%M"):
                    schedule.slot_1430 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("15:00", "%H:%M"):
                    schedule.slot_1500 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("15:30", "%H:%M"):
                    schedule.slot_1530 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("16:00", "%H:%M"):
                    schedule.slot_1600 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("16:30", "%H:%M"):
                    schedule.slot_1630 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("17:00", "%H:%M"):
                    schedule.slot_1700 = False
                elif datetime.datetime.strptime(precord.appointment_time.strftime("%H:%M"), "%H:%M") == datetime.datetime.strptime("17:30", "%H:%M"):
                    schedule.slot_1730 = False
                schedule.save()
            counter += 1


    if slot == "schedule.slot_800":
        schedule.slot_800 = False
    elif slot == "schedule.slot_830":
        schedule.slot_830 = False
    elif slot == "schedule.slot_900":
        schedule.slot_900 = False
    elif slot == "schedule.slot_930":
        schedule.slot_930 = False
    elif slot == "schedule.slot_1000":
        schedule.slot_100 = False
    elif slot == "schedule.slot_1030":
        schedule.slot_1030 = False
    elif slot == "schedule.slot_1100":
        schedule.slot_1100 = False
    elif slot == "schedule.slot_1130":
        schedule.slot_1130 = False
    elif slot == "schedule.slot_1200":
        schedule.slot_1200 = False
    elif slot == "schedule.slot_1230":
        schedule.slot_1230 = False
    elif slot == "schedule.slot_1400":
        schedule.slot_1400 = False
    elif slot == "schedule.slot_1430":
        schedule.slot_1430 = False
    elif slot == "schedule.slot_1500":
        schedule.slot_1500 = False
    elif slot == "schedule.slot_1530":
        schedule.slot_1530 = False
    elif slot == "schedule.slot_1600":
        schedule.slot_1600 = False
    elif slot == "schedule.slot_1630":
        schedule.slot_1630 = False
    elif slot == "schedule.slot_1700":
        schedule.slot_1700 = False
    elif slot == "schedule.slot_1730":
        schedule.slot_1730 = False
    schedule.save()
    record.doctor = doctor
    record.appointment_date = datetime.date.today()
    record.appointment_time = time
    record.save()

    context = {
        "doctor": doctor,
        "time": time,
        "date": datetime.date.today(),
    }
    return render(request, "patient/bookingConfirmed.html", context)


def assign_criticality(age, gender, past_history, current_symptoms):
    score = 0
    
    if int(age) >= 60:
        score += 2
    elif int(age) >= 40:
        score += 1
    
    if gender.lower() == "male":
        score += 1
    
    if "diabetes" in past_history.lower():
        score += 2
    elif "hypertension" in past_history.lower():
        score += 1
    
    if "difficulty breathing" in current_symptoms.lower() or "shortness of breath" in current_symptoms.lower():
        score += 2
    elif "fever" in current_symptoms.lower() or "cough" in current_symptoms.lower() or "sore throat" in current_symptoms.lower():
        score += 1
    
    # Assign criticality score
    if score <= 3:
        return 1
    elif score <= 6:
        return 2
    elif score <= 9:
        return 3
    elif score <= 12:
        return 4
    else:
        return 5


def predictCriticality(age = 40, gender = 'Male',	diabetes_history = 'No',	hypertension_history = 'No',
                        fever = 'Yes',	cough = 'Yes',	sore_throat = 'No',	difficulty_breathing = 'No',
                        shortness_of_breath = 'No'):
    pickled_model = pickle.load(open('patient/criticality_model.pkl', 'rb'))
    gen = 1
    dh = 0
    hh = 0
    fev = 1
    cough = 1
    stt = 0
    db = 0
    sob = 0
    if gender == 'Male':
        gen = 1
    else:
        gen = 0
    if diabetes_history == "Yes":
        dh = 1
    else:
        dh = 0
    if hypertension_history == "Yes":
        hh = 1
    else:
        hh = 0
    if fever == "Yes":
        fev = 1
    else:
        fev = 0
    if cough == "Yes":
        cough = 1
    else:
        cough = 0
    if sore_throat == "Yes":
        stt = 1
    else:
        stt = 0
    if difficulty_breathing == "Yes":
        db = 1
    else:
        db = 0
    if shortness_of_breath == "Yes":
        sob = 1
    else:
        sob = 0
    list = pickled_model.predict([[age, gen, dh, hh, fev, cough, stt, db, sob]])
    if list[0] == 1:
        return 1
    elif list[0] == 2:
        return 2
    elif list[0] == 3:
        return 3
    elif list[0] == 4:
        return 4
    else:
        return 5
  

def fetchNearestTimeSlot(schedule, time):
    time_to_allot = None
    if time == "08:00" and schedule.slot_800 == True:
        time_to_allot = "schedule.slot_800"
    elif time == "08:30" and schedule.slot_830 == True:
        time_to_allot = "schedule.slot_830"
    elif time == "09:00" and schedule.slot_900 == True:
        time_to_allot = "schedule.slot_900"
    elif time == "09:30" and schedule.slot_930 == True:
        time_to_allot = "schedule.slot_930"
    elif time == "10:00" and schedule.slot_1000 == True:
        time_to_allot = "schedule.slot_1000"
    elif time == "10:30" and schedule.slot_1030 == True:
        time_to_allot = "schedule.slot_1030"
    elif time == "11:00" and schedule.slot_1100 == True:
        time_to_allot = "schedule.slot_1100"
    elif time == "11:30" and schedule.slot_1130 == True:
        time_to_allot = "schedule.slot_1130"
    elif time == "12:00" and schedule.slot_1200 == True:
        time_to_allot = "schedule.slot_1200"
    elif time == "12:30" and schedule.slot_1230 == True:
        time_to_allot = "schedule.slot_1230"
    elif time == "14:00" and schedule.slot_1400 == True:
        time_to_allot = "schedule.slot_1400"
    elif time == "14:30" and schedule.slot_1430 == True:
        time_to_allot = "schedule.slot_1430"
    elif time == "15:00" and schedule.slot_1500 == True:
        time_to_allot = "schedule.slot_1500"
    elif time == "15:30" and schedule.slot_1530 == True:
        time_to_allot = "schedule.slot_1530"
    elif time == "16:00" and schedule.slot_1600 == True:
        time_to_allot = "schedule.slot_1600"
    elif time == "16:30" and schedule.slot_1630 == True:
        time_to_allot = "schedule.slot_1630"
    elif time == "17:00" and schedule.slot_1700 == True:
        time_to_allot = "schedule.slot_1700"
    elif time == "17:30" and schedule.slot_1730 == True:
        time_to_allot = "schedule.slot_1730"
    return time_to_allot