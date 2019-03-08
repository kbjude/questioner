from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import Index

urlpatterns = [
    path('', Index.as_view()),
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
]
