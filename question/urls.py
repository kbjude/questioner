from django.urls import path

from question.views import Questions, OneQuestion

urlpatterns = [
    path("<meetup_id>/questions/", Questions.as_view(), name="questions"),
    path(
        "<meetup_id>/questions/<question_id>/",
        OneQuestion.as_view(),
        name="question",
    ),
]
