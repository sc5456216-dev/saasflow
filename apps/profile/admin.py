from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone', 'email_verified']
    search_fields = ['user__username', 'user__email']
    list_filter = ['email_verified']
