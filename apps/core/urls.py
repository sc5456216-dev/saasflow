from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/health/', views.api_health, name='api_health'),
]
