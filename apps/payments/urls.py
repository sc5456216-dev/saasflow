from django.urls import path
from . import views

urlpatterns = [
    path('payment/create-checkout/<str:plan_id>/', views.create_checkout_session, name='create_checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment/billing/', views.billing_history, name='billing'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
