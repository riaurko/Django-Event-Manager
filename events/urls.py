from django.urls import path
from events.views import *

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('<int:event_id>/rsvp/<int:user_id>', rsvp_event, name="rsvp"),
    path('create-event/', create_event, name="create-event"),
    path('create-category/', create_category, name="create-category"),
    path('view-events/', view_events, name="view-event"),
    path('view-categories/', view_categories, name="view-category"),
    path('update-event/<int:id>', update_event, name="update-event"),
    path('update-category/<int:id>', update_category, name="update-category"),
    path('delete-event/<int:id>', delete_event, name="delete-event"),
    path('delete-category/<int:id>', delete_category, name="delete-category"),
    path('event-info/<int:id>', event_details, name="event-details"),
]
