from django.urls import path
from events.views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('new-event/', create_event, name="create-event"),
    path('new-category/', create_category, name="create-category"),
    path('new-participant/', create_participant, name="create-participant"),
    path('all-events/', view_events, name="view-event"),
    path('all-categories/', view_categories, name="view-category"),
    path('all-participants/', view_participants, name="view-participant"),
    path('update-event/<int:id>', update_event, name="update-event"),
    path('update-category/<int:id>', update_category, name="update-category"),
    path('update-participant/<int:id>', update_participant, name="update-participant"),
    path('delete-event/<int:id>', delete_event, name="delete-event"),
    path('delete-category/<int:id>', delete_category, name="delete-category"),
    path('delete-participant/<int:id>', delete_participant, name="delete-participant"),
    path('event-info/<int:id>', event_details, name="event-details"),
]
