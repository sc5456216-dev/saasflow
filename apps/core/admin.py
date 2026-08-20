from django.contrib import admin
from .models import Company, Subscription

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at', 'is_active']
    search_fields = ['name', 'owner__username']
    list_filter = ['is_active', 'created_at']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['company', 'plan', 'status', 'start_date', 'end_date']
    list_filter = ['plan', 'status']
    search_fields = ['company__name']
