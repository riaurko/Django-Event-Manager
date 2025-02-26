from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count, Q, Prefetch
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from datetime import date
from users.forms import UserSignUp, UserLogin, AssignRole, CreateGroup
from events.models import Event

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def sign_up(request):
    form = UserSignUp()
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, "A Verification Mail has been sent to your Email. Please check.")
            return redirect('login')
    return render(request, "registration/sign_up.html", {'form': form})

def log_in(request):
    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("land")
    return render(request, "registration/login.html", {'form': form})

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse("<h3>Invalid Id or Token</h3>")
    except User.DoesNotExist:
        return HttpResponse("<h3>404: Not Found<br/>User Not Found</h3>")


@login_required
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect("login")

@permission_required("users.add_group", 'no-access')
def create_group(request):
    form = CreateGroup()
    if request.method == 'POST':
        form = CreateGroup(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"New Group {group.name} created successfully")
            return redirect("create-group")
    return render(request, "admin/create_group.html", {'form': form})

@user_passes_test(is_admin, 'no-access')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRole()
    if request.method == 'POST':
        form = AssignRole(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username} is successfully assigned to {role.name} Role.")
    return render(request, "admin/assign_role.html", {'form': form})

@permission_required("users.view_group", 'no-access')
def view_group(request):
    groups = Group.objects.prefetch_related('permissions').all().order_by('name')
    return render(request, "admin/view_group.html", {'groups': groups})

@login_required
@user_passes_test(is_admin, 'no-access')
def admin_dashboard(request):
    users = User.objects.prefetch_related(Prefetch('groups', Group.objects.all(), 'all_groups')).all().order_by('id')
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'N/A'
    return render(request, "admin/dashboard.html", {'users': users})

@login_required
@user_passes_test(is_organizer, 'no-access')
def organizer_dashboard(request):
    event_type = request.GET.get('type', 'today')
    events_count = Event.objects.aggregate(counter=Count('id'))
    past_events = Event.objects.filter(date__gte=date.fromisoformat("2025-01-01"), date__lt=date.today()).aggregate(counter=Count('id'))
    future_events = Event.objects.filter(date__gt=date.today(), date__lte=date.fromisoformat("2034-12-31")).aggregate(counter=Count('id'))
    participants_count = User.objects.aggregate(counter=Count('id'))
    base_event_query = Event.objects.annotate(partice_count=Count('participants')).select_related('category').prefetch_related('participants')

    if event_type == 'all':
        events = base_event_query.all()
    elif event_type == 'today':
        events = base_event_query.filter(date=date.today())
    elif event_type == 'upcoming':
        events = base_event_query.filter(date__gte=date.today(), date__lte=date.fromisoformat("2034-12-31"))
    elif event_type == 'past':
        events = base_event_query.filter(date__gte=date.fromisoformat("2025-01-01"), date__lte=date.today())
    
    context = {
        'events': events,
        'past_events': past_events,
        'upcoming_events': future_events,
        'total_events': events_count,
        'total_participants': participants_count,
    }
    return render(request, "organizer/dashboard.html", context)

@login_required
@user_passes_test(is_participant, 'no-access')
def participant_dashboard(request):
    pass
