from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.cache import never_cache
from apps.core.models import Company, Subscription

@csrf_protect
@ensure_csrf_cookie
@never_cache
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'dashboard/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')  # Redirect to login page

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'dashboard/register.html')

@login_required(login_url='/login/')
def dashboard(request):
    try:
        company = Company.objects.get(owner=request.user)
        subscription = Subscription.objects.filter(company=company, status='active').first()
    except Company.DoesNotExist:
        company = None
        subscription = None
    
    context = {
        'company': company,
        'subscription': subscription,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='/login/')
def create_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website')
        
        if name:
            company = Company.objects.create(
                name=name,
                website=website,
                owner=request.user
            )
            messages.success(request, f'Company "{name}" created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Company name is required.')
    
    return render(request, 'dashboard/create_company.html')

@login_required(login_url='/login/')
def view_plans(request):
    plans = [
        {
            'id': 'starter',
            'name': 'Starter',
            'price': '',
            'period': '/mo',
            'features': ['5 Team Members', '10 Projects', 'Basic Analytics', 'Email Support'],
            'popular': False
        },
        {
            'id': 'professional',
            'name': 'Professional',
            'price': '',
            'period': '/mo',
            'features': ['20 Team Members', 'Unlimited Projects', 'Advanced Analytics', 'Priority Support', 'API Access'],
            'popular': True
        },
        {
            'id': 'enterprise',
            'name': 'Enterprise',
            'price': '',
            'period': '/mo',
            'features': ['Unlimited Team', 'Unlimited Projects', 'Custom Analytics', '24/7 Phone Support', 'Dedicated Account'],
            'popular': False
        }
    ]
    
    try:
        company = Company.objects.get(owner=request.user)
        current_subscription = Subscription.objects.filter(company=company, status='active').first()
    except Company.DoesNotExist:
        company = None
        current_subscription = None
    
    context = {
        'plans': plans,
        'current_subscription': current_subscription,
        'company': company,
    }
    return render(request, 'dashboard/plans.html', context)

@login_required(login_url='/login/')
def subscribe(request, plan_id):
    try:
        company = Company.objects.get(owner=request.user)
        
        existing_subscription = Subscription.objects.filter(company=company, status='active').first()
        
        if existing_subscription:
            existing_subscription.status = 'cancelled'
            existing_subscription.save()
            messages.info(request, f'Previous subscription to {existing_subscription.get_plan_display()} was cancelled.')
        
        plan_map = {
            'starter': 'starter',
            'professional': 'professional',
            'enterprise': 'enterprise'
        }
        
        subscription = Subscription.objects.create(
            company=company,
            plan=plan_map.get(plan_id, 'starter'),
            status='active',
            auto_renew=True
        )
        
        messages.success(request, f'Successfully subscribed to {subscription.get_plan_display()} plan!')
        return redirect('dashboard')
        
    except Company.DoesNotExist:
        messages.error(request, 'Please create a company first before subscribing to a plan.')
        return redirect('create_company')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('plans')
# Add to apps/dashboard/views.py
from apps.products.models import Order, Wishlist, Product
from apps.core.models import Company, Subscription

@login_required(login_url='/login/')
def dashboard_stats(request):
    """Get user statistics for dashboard"""
    user = request.user
    
    # Order statistics
    orders = Order.objects.filter(user=user)
    order_count = orders.count()
    total_spent = orders.aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    # Wishlist count
    wishlist_count = Wishlist.objects.filter(user=user).count()
    
    # Company info
    company = Company.objects.filter(owner=user).first()
    subscription = Subscription.objects.filter(company=company, status='active').first() if company else None
    
    # Recently viewed products
    recently_viewed = RecentlyViewed.objects.filter(user=user).select_related('product')[:5]
    
    context = {
        'order_count': order_count,
        'total_spent': total_spent,
        'wishlist_count': wishlist_count,
        'company': company,
        'subscription': subscription,
        'recently_viewed': recently_viewed,
    }
    return JsonResponse(context)
