"""questioner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name="welcome"),
    url(r'^admin/', admin.site.urls),
    path(r'^auth/login/$', obtain_auth_token, name='api_token_auth'),
    url(r'^meetups/', include('meetup.urls')),
    url(r'^questions/', include('question.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns = [
    # path('questions', views.questions),
    # path('questions/<question_id>', views.question)
# ]

