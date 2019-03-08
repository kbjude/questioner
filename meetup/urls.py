<<<<<<< HEAD
from django.urls import path
from .views import Index, SignUp, Login


urlpatterns = [
    path('', Index.as_view()),
    path('auth/login/', Login.as_view(), name='login'),
    path('auth/signup/', SignUp.as_view(), name='signup'),
=======
from django.conf.urls import url
from . import views


urlpatterns = [
    # /meetups/
    url(r'^$', views.MeetingList.as_view(), name='meetings'),

    # /meetups/234/
    url(r'^(?P<meeting_id>[0-9]+)$',
        views.AMeeting.as_view(), name='meeting'),
>>>>>>> upstream/develop
]
