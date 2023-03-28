from django.db import reset_queries
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Profile, ProfileType
from patient.models import Patient
from doctor.models import Doctor
from django.contrib import messages
from twilio.rest import Client

account_sid = "AC55c9a8f627d04846c4bd32cac3c5ce42"
auth_token = "c170335832079fcebf31604ab106452e"
verify_sid = "VAaccccf3dea88375ee2d023708ddc8699"
client = Client(account_sid, auth_token)


def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        phone_nos_in_database = list(
            Profile.objects.all().values_list('phone', flat=True))
        if phone not in phone_nos_in_database:
            messages.info(request, 'Phone number not registered')
            print("Phone number is not registered in the database, Create a new user")
            print("Do you want to create a new user")
            return redirect('register_phone')
        else:
            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=phone, channel="sms")
            print("OTP sent to the phone number")
            return redirect('verifyOTP', create_user='login', phone=phone)
    else:
        return render(request, 'accounts/login.html')


def verifyOTP(request, create_user, phone):
    if request.method == 'POST':
        otp = request.POST['otp']
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone, code=otp)
        print("Entered OTP: ", otp)
        print("Verification Status: ", verification_check.status)
        if create_user == 'login':
            if verification_check.status == 'approved':
                return redirect('authenticate', phone=phone)
            else:
                messages.info(request, 'Incorrect OTP')
                print("Incorrect OTP has been entered")
                return redirect('verifyOTP', create_user='login', phone=phone)
        else:
            if verification_check.status == 'approved':
                return redirect('register_profile', phone=phone)
            else:
                messages.info(request, 'Incorrect OTP')
                print("Incorrect OTP has been entered")
                return redirect('verifyOTP', create_user='register', phone=phone)
    else:
        return render(request, 'accounts/verifyOTP.html')


def authenticate(request, phone):
    profile = Profile.objects.get(phone=phone)
    user = profile.user
    auth.login(request, user)
    print("**User has been authenticated**")
    print("User: ", request.user)
    return redirect('profile')


def register_phone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=phone, channel="sms")
        print("OTP sent to the phone number")
        return redirect('verifyOTP', create_user='register', phone=phone)
    else:
        return render(request, 'accounts/register_phone.html')

def register_profile(request, phone):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        profile_type = request.POST['profile_type']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('register_profile', phone=phone)
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email ID already exists')
            return redirect('register_profile', phone=phone)
        else:
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email)
            user.save()
            profile = Profile.objects.create(
                user=user, phone=phone, profile_type=ProfileType.objects.get(type=profile_type))
            profile.save()
            if profile_type == "Patient":
                patient = Patient.objects.create(profile=profile)
                patient.save()
            elif profile_type == "Doctor":
                doctor = Doctor.objects.create(profile=profile)
                doctor.save()
            return redirect('authenticate', phone=phone)
    else:
        return render(request, 'accounts/register_profile.html')


def logout(request):
    auth.logout(request)
    print("User has been logged out")
    return redirect('login')


def profile(request):
    user = request.user
    name = user.first_name + ' ' + user.last_name
    email = user.email
    context = {'name': name, 'email': email}
    return render(request, 'accounts/profile.html', context)
