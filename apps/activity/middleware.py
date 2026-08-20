from django.utils.deprecation import MiddlewareMixin
from .models import ActivityLog

class ActivityLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return
        
        # Log user activity
        if request.user.is_authenticated:
            action = None
            path = request.path
            
            if path == '/login/':
                action = 'login'
            elif path == '/logout/':
                action = 'logout'
            elif path == '/register/':
                action = 'register'
            elif path == '/profile/edit/':
                action = 'profile_update'
            elif path == '/dashboard/create-company/':
                action = 'company_create'
            
            if action:
                ActivityLog.objects.create(
                    user=request.user,
                    action=action,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    metadata={'path': path, 'method': request.method}
                )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
