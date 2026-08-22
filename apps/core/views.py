from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'core/home.html')

def api_health(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'SaaSFlow API is running!',
        'version': '1.0.0'
    })
# Add to apps/core/views.py
from .models import Newsletter
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                newsletter, created = Newsletter.objects.get_or_create(email=email)
                if created:
                    return JsonResponse({'success': True, 'message': 'Subscribed successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Already subscribed.'})
            except:
                return JsonResponse({'success': False, 'message': 'Error subscribing.'})
    return JsonResponse({'success': False, 'message': 'Invalid email.'})
