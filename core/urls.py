from django.urls import path
from core.views import landing_page, no_access

urlpatterns = [
    path('', landing_page, name="land"),
    path('no-access/', no_access, name="no-access"),
]
