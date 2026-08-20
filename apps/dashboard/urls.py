from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Use custom logout
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create-company/', views.create_company, name='create_company'),
    path('dashboard/plans/', views.view_plans, name='plans'),
    path('dashboard/subscribe/<str:plan_id>/', views.subscribe, name='subscribe'),
]
