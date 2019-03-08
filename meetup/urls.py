from django.conf.urls import url
from . import views


urlpatterns = [
    # /meetups/
    url(r'^$', views.MeetingList.as_view(), name='meetings'),

    # /meetups/234/
    url(r'^(?P<meeting_id>[0-9]+)$',
        views.AMeeting.as_view(), name='meeting'),
]
