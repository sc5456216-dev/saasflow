from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('profile_update', 'Profile Update'),
        ('company_create', 'Company Created'),
        ('company_update', 'Company Updated'),
        ('subscription_create', 'Subscription Created'),
        ('subscription_cancel', 'Subscription Cancelled'),
        ('payment_success', 'Payment Success'),
        ('payment_failed', 'Payment Failed'),
        ('team_create', 'Team Created'),
        ('team_member_add', 'Team Member Added'),
        ('team_member_remove', 'Team Member Removed'),
        ('password_reset', 'Password Reset'),
        ('email_verified', 'Email Verified'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.get_action_display()} - {self.created_at}"
