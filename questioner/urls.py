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
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.urls import path
from meetup import views as meetup_views
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="welcome"),
    path("auth/login", views.Login.as_view(), name="login"),
    path("auth/signup", views.SignUp.as_view(), name="signup"),
    path("meetups/", include("meetup.urls")),
    path("meetups/", include("question.urls")),
    path('tags/', meetup_views.TagList.as_view(), name='tags'),
    path('tags/<int:tag_id>', meetup_views.ATag.as_view(), name='tag'),
    path('admin/', admin.site.urls),

]

urlpatterns = format_suffix_patterns(urlpatterns)
