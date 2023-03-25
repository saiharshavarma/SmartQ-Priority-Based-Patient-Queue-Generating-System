from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('verify/<create_user>/<phone>', views.verifyOTP, name="verifyOTP"),
    path('authenticate/<phone>', views.authenticate, name="authenticate"),
    path('register_phone', views.register_phone, name="register_phone"),
    path('register_profile/<phone>', views.register_profile, name="register_profile"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
]
