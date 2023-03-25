from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class ProfileType(models.Model):
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.type)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, unique=True)
    profile_type = models.ForeignKey(
        ProfileType, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.user.id}' + ' ' + f'{self.user.username}' + ' ' + f'{self.phone}' + ' ' + f'{self.profile_type}')
