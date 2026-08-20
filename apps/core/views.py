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
