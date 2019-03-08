from django.urls import path
from .views import Index, SignUp, Login


urlpatterns = [
    path('', Index.as_view()),
    path('auth/login/', Login.as_view(), name='login'),
    path('auth/signup/', SignUp.as_view(), name='signup'),
]
