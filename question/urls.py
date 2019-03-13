from django.urls import path

from question.views import Questions, OneQuestion, CommentList, CommentDetail

urlpatterns = [
    path("<meetup_id>/questions/", Questions.as_view(), name="questions"),
    path(
        "<meetup_id>/questions/<question_id>/",
        OneQuestion.as_view(),
        name="question",
    ),
    path(
        "<meetup_id>/questions/<question_id>/comments",
        CommentList.as_view(), name="comment",
    ),
    path(
        "<meetup_id>/questions/<question_id>/comments/<int:pk>",
        CommentDetail.as_view(), name="comment_details"
    ),
]
