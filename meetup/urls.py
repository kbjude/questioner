from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    # /meetups/
    path('meetings/', views.MeetingList.as_view(), name='meetings'),

    # /meetups/234/
    path('meentings/<meeting_id>/',
         views.AMeeting.as_view(), name='meeting'),
]
