from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models import Company, Subscription
from apps.profile.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'phone', 'avatar', 'email_verified', 'created_at']

class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'owner', 'is_active', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'company', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
