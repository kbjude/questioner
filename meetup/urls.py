from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Index, SignUp


urlpatterns = [
    path('', Index.as_view()),
    path('auth/login/', obtain_auth_token, name='login'),
    path('auth/signup', SignUp.as_view(), name='signup'),
]
