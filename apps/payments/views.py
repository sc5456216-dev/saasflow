import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from apps.core.models import Company, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='/login/')
def create_checkout_session(request, plan_id):
    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'Please create a company first')
        return redirect('create_company')
    
    plan_config = {
        'starter': {
            'price_id': 'price_starter_id',
            'amount': 2900,
            'name': 'Starter'
        },
        'professional': {
            'price_id': 'price_professional_id',
            'amount': 7900,
            'name': 'Professional'
        },
        'enterprise': {
            'price_id': 'price_enterprise_id',
            'amount': 19900,
            'name': 'Enterprise'
        }
    }
    
    plan = plan_config.get(plan_id)
    if not plan:
        messages.error(request, 'Invalid plan selected')
        return redirect('plans')
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"{plan['name']} Plan - SaaSFlow",
                        'description': f'Monthly subscription to {plan["name"]} plan',
                    },
                    'unit_amount': plan['amount'],
                    'recurring': {
                        'interval': 'month',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
            client_reference_id=request.user.id,
            metadata={
                'user_id': request.user.id,
                'company_id': company.id,
                'plan': plan_id,
            },
        )
        
        return redirect(checkout_session.url)
        
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('plans')

@login_required(login_url='/login/')
def payment_success(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'Invalid session')
        return redirect('dashboard')
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        user_id = session.metadata.get('user_id')
        company_id = session.metadata.get('company_id')
        plan = session.metadata.get('plan')
        
        if user_id and company_id and plan:
            company = Company.objects.get(id=company_id)
            Subscription.objects.filter(company=company, status='active').update(status='cancelled')
            Subscription.objects.create(
                company=company,
                plan=plan,
                status='active',
                auto_renew=True
            )
            messages.success(request, f'Successfully subscribed to {plan.title()} plan!')
        else:
            messages.info(request, 'Payment completed but subscription needs to be activated.')
            
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
    
    return redirect('dashboard')

@login_required(login_url='/login/')
def payment_cancel(request):
    messages.info(request, 'Payment was cancelled.')
    return redirect('plans')

@login_required(login_url='/login/')
def billing_history(request):
    try:
        company = Company.objects.get(owner=request.user)
        subscriptions = Subscription.objects.filter(company=company)
    except Company.DoesNotExist:
        subscriptions = None
    
    context = {'subscriptions': subscriptions}
    return render(request, 'payments/billing.html', context)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
    
    return JsonResponse({'status': 'success'})
