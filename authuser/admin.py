from django.contrib import admin

# Register your models here
from .models import UserProfile, EmailVerification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    pass