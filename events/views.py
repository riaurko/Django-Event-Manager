from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from datetime import date
from events.models import *
from events.forms import CreateEvent, CreateCategory
from users.views import is_admin, is_organizer, is_participant

#* Role-Based Dashboard
@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-db')
    elif is_organizer(request.user):
        return redirect('organizer-db')
    elif is_participant(request.user):
        return redirect('participant-db')

@permission_required("events.create_event", 'no-access')
#* Event Creation View
def create_event(request):
    categories = Category.objects.all()
    form = CreateEvent(categories=categories)
    if request.method == "POST":
        form = CreateEvent(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Bravo! New Event Created Successfully.")
    context = {'form': form}
    return render(request, "create_event.html", context)

@permission_required("events.create_category", 'no-access')
#* Category Creation View
def create_category(request):
    form = CreateCategory()
    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bravo! Category Created Successfully.")
        else:
            messages.error(request, "Sorry Brother! Category with that Name already exist.")
    context = {'form': form}
    return render(request, 'create_category.html', context)

#* All Event Viewing View
def view_events(request):
    search_q = request.GET.get('search', 'all')
    category_q = request.GET.get('category', 'all')
    date_q_start = request.GET.get('start_date', '2025-01-01')
    date_q_end = request.GET.get('end_date', '2034-12-31')
    # print(search_q, category_q, date_q_start, date_q_end)
    base_q = Event.objects.annotate(partice_count=Count('participants')).select_related('category')
    categories = Category.objects.all()
    if search_q == 'all' or search_q == '':
        events = base_q.all()
    else:
        events = base_q.filter(Q(name__icontains=search_q) | Q(location__icontains=search_q))
    if category_q == 'all':
        events = events.all()
    else:
        events = events.filter(category__name__contains=category_q)
    if date_q_start == '':
        events = events.all()
    else:
        events = events.filter(date__range=[date_q_start, date_q_end])
    return render(request, 'view_events.html', {'events': events, 'categories': categories})

@permission_required("events.view_category", 'no-access')
#* All Category Viewing View
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'view_categories.html', {'categories': categories})

@permission_required("events.update_event", 'no-access')
#* Event Updating View
def update_event(request, id):
    event = Event.objects.get(id=id)
    categories = Category.objects.all()
    form = CreateEvent(categories=categories, instance=event)
    if request.method == "POST":
        form = CreateEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Okay! Event Updated Successfully.")
    context = {'form': form}
    return render(request, "create_event.html", context)

@permission_required("events.update_category", 'no-access')
#* Category Updating View
def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CreateCategory(instance=category)
    if request.method == "POST":
        form = CreateCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Okay! Category Updated Successfully.")
        else:
            messages.error(request, "Sorry Brother! Category with that Name already exist.")
    context = {'form': form}
    return render(request, 'create_category.html', context)

#* Participant Updating View
# def update_participant(request, id):
#     participant = Participant.objects.get(id=id)
#     form = CreateParticipant(instance=participant)
#     if request.method == "POST":
#         form = CreateParticipant(request.POST, instance=participant)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Okay! Participant Info Updated.")
#         else:
#             messages.error(request, "Hey, don't coopyy another's Email!")
#     context = {'form': form}
    return render(request, 'create_participant.html', context)

@permission_required("events.delete_event", 'no-access')
#* Event Deleting View
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Bye Bye Event!")
        return redirect('view-event')
    else:
        messages.error(request, "Shit, Something went Wrong!")

@permission_required("events.delete_category", 'no-access')
#* Category Deleting View
def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Bye Bye Category!")
        return redirect('view-category')
    else:
        messages.error(request, "Shit, Something went Wrong!")

#* Participant Deleting View
# def delete_participant(request, id):
#     if request.method == 'POST':
#         participant = Participant.objects.get(id=id)
#         participant.delete()
#         messages.success(request, "Bye Bye Participant!")
#         return redirect('view-participant')
#     else:
#         messages.error(request, "Shit, Something went Wrong!")

#* Event Details View
def event_details(request, id):
    event = Event.objects.annotate(partice_count=Count('participants')).get(id=id)
    participants = event.participants.all()
    return render(request, "event_details.html", {'event': event, 'participants': participants})

#* Event RSVP View
@login_required
# @user_passes_test(is_participant, 'no-access')
def rsvp_event(request, user_id, event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event.participants.filter(id=user_id).exists():
        event.participants.add(user_id)
        return redirect('view-event')
    else:
        return redirect('no-access')
