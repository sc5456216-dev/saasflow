from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import ActivityLog

@login_required(login_url='/login/')
@staff_member_required
def activity_log(request):
    logs = ActivityLog.objects.all()[:100]
    return render(request, 'activity/activity_log.html', {'logs': logs})
