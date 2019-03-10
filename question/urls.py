from django.urls import path
from . import views


urlpatterns = [
    path('<meetup_id>/questions', views.questions),
    path('<meetup_id>/questions/<question_id>', views.question)
]
