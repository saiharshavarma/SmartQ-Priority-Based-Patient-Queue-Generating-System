from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.getPhoneNumber, name="login"),
    path('verify', views.verifyOTP, name="verifyOTP"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
]
