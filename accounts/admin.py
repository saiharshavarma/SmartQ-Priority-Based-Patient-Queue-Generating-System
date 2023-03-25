from django.contrib import admin
from .models import Profile, ProfileType


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'phone', 'profile_type')


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileType)
