from django.urls import path

from . import views

urlpatterns = [
    # /meetups/
    path("", views.MeetingList.as_view(), name="meetings"),
    # /meetups/234/
    path("<meeting_id>/", views.AMeeting.as_view(), name="meeting"),
]
