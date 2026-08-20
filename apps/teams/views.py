from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from apps.core.models import Company
from .models import Team, TeamMember

@login_required(login_url='/login/')
def team_list(request):
    try:
        company = Company.objects.get(owner=request.user)
        teams = Team.objects.filter(company=company)
    except Company.DoesNotExist:
        messages.error(request, 'Please create a company first')
        return redirect('create_company')
    
    context = {'teams': teams, 'company': company}
    return render(request, 'teams/team_list.html', context)

@login_required(login_url='/login/')
def team_create(request):
    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'Please create a company first')
        return redirect('create_company')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            team = Team.objects.create(
                name=name,
                description=description,
                company=company,
                created_by=request.user
            )
            TeamMember.objects.create(
                team=team,
                user=request.user,
                role='admin'
            )
            messages.success(request, f'Team "{name}" created successfully!')
            return redirect('team_list')
        else:
            messages.error(request, 'Team name is required.')
    
    return render(request, 'teams/team_create.html')

@login_required(login_url='/login/')
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    members = TeamMember.objects.filter(team=team)
    
    is_member = TeamMember.objects.filter(team=team, user=request.user).exists()
    user_role = None
    if is_member:
        user_role = TeamMember.objects.get(team=team, user=request.user).role
    
    context = {
        'team': team,
        'members': members,
        'is_member': is_member,
        'user_role': user_role
    }
    return render(request, 'teams/team_detail.html', context)

@login_required(login_url='/login/')
def team_add_member(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    try:
        membership = TeamMember.objects.get(team=team, user=request.user)
        if membership.role != 'admin':
            messages.error(request, 'Only admins can add members.')
            return redirect('team_detail', team_id=team.id)
    except TeamMember.DoesNotExist:
        messages.error(request, 'You are not a member of this team.')
        return redirect('team_detail', team_id=team.id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('role', 'member')
        
        try:
            user = User.objects.get(username=username)
            if TeamMember.objects.filter(team=team, user=user).exists():
                messages.error(request, f'{username} is already in this team.')
            else:
                TeamMember.objects.create(
                    team=team,
                    user=user,
                    role=role
                )
                messages.success(request, f'{username} added to team successfully!')
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
        
        return redirect('team_detail', team_id=team.id)
    
    return render(request, 'teams/team_add_member.html', {'team': team})
