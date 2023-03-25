from django.db import reset_queries
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Profile, ProfileType
from django.contrib import messages
from twilio.rest import Client
import os
import random

account_sid = "AC55c9a8f627d04846c4bd32cac3c5ce42"
auth_token = "2652cb28e9edfd850d24938bdfbe4877"
verify_sid = "VAaccccf3dea88375ee2d023708ddc8699"
client = Client(account_sid, auth_token)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        profile_type = request.POST['profile_type']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email ID already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                user.save()
                profile = Profile.objects.create(
                    user=user, phone=phone, profile_type=profile_type)
                profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not matching')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def getPhoneNumber(request):
    if request.method == 'GET':
        # phone = request.POST['phone']
        phone = '+919049917706'
        phone_nos_in_database = list(
            Profile.objects.all().values_list('phone', flat=True))
        if phone not in phone_nos_in_database:
            messages.info(request, 'Phone number not registered')
            print("Phone number is not registered in the database, Create a new user")
            print("Do you want to create a new user")
            # verifyOTP
            # redirect register
            return render(request, 'accounts/login.html')
        else:
            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=phone, channel="sms")
            print("OTP sent to the phone number")
            return redirect('verifyOTP')
    else:
        return render(request, 'accounts/login.html')


def verifyOTP(request, phone='+919049917706'):
    if request.method == 'POST':
        otp = request.POST['otp']
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone, code=otp)
        print("Entered OTP: ", otp)
        print("Verification Status: ", verification_check.status)
        if verification_check.status == 'approved':
            login(request, verification_check.status, phone)
            return render(request, 'accounts/login.html')
        else:
            messages.info(request, 'Incorrect OTP')
            print("Incorrect OTP has been entered")
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/verifyOTP.html')


def login(request, status, phone):
    profile = Profile.objects.get(phone=phone)
    user = profile.user
    auth.login(request, user)
    print("**User has been authenticated**")
    print("User: ", request.user)
    return True


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
