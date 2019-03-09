from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('auth/login/', views.Login.as_view(), name='login'),
    path('auth/signup/', views.SignUp.as_view(), name='signup'),

    # /meetups/
    path('meetings/', views.MeetingList.as_view(), name='meetings'),

    # /meetups/234/
    path('meentings/<meeting_id>/',
         views.AMeeting.as_view(), name='meeting'),
]
