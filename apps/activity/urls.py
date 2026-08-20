from django.urls import path
from . import views

urlpatterns = [
    path('activity/', views.activity_log, name='activity_log'),
]
