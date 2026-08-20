from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

@login_required(login_url='/login/')
def profile_view(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'profile/profile.html', context)

@login_required(login_url='/login/')
def profile_edit(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email')
        user.save()
        
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.phone = request.POST.get('phone', '')
        
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile
    }
    return render(request, 'profile/profile_edit.html', context)
