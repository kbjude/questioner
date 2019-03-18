from django.urls import path

from . import views

urlpatterns = [
    # /meetups/
    path("", views.MeetingList.as_view(), name="meetings"),
    # /meetups/234/
    path("<int:meeting_id>", views.AMeeting.as_view(), name="meeting"),
    # /meetups/{meet_up_id}tags/
    path(
        "<int:meeting_id>/tags/",
        views.AddMeetupTag.as_view(),
        name="meetingtags",
    ),
    # /meetups/234/tags/432
    path(
        "<int:meeting_id>/tags/<int:tag_id>",
        views.AmeetupTag.as_view(),
        name="meetingtag",
    ),

]
