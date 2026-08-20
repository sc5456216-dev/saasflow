from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.profile.urls')),
    path('', include('apps.teams.urls')),
    path('', include('apps.payments.urls')),
    path('', include('apps.activity.urls')),
    
    # Redirect accounts/login to our login page
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
