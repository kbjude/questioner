from django.urls import path

from question.views import (Questions, OneQuestion, Votes,
                            CommentList, CommentDetail)

urlpatterns = [
    path("<int:meetup_id>/questions/", Questions.as_view(), name="questions"),
    path(
        "<int:meetup_id>/questions/<int:question_id>/",
        OneQuestion.as_view(),
        name="question",
    ),
    path(
        "<int:meetup_id>/questions/<int:question_id>/votes/",
        Votes.as_view(),
        name="votes",
    ),
    path("<int:meetup_id>/questions/<question_id>/comments",
        CommentList.as_view(),
    ),
    path("<int:meetup_id>/questions/<question_id>/comments/<int:pk>",
        CommentDetail.as_view(),
    )
]
