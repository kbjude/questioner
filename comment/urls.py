from django.urls import path
from comment.views import CommentList, CommentDetail, ToggleAnswer

urlpatterns = [
    path("<int:meetup_id>/questions/<question_id>/comments",
         CommentList.as_view(), name='comment'),
    path("<int:meetup_id>/questions/<question_id>/comments/<int:pk>",
         CommentDetail.as_view(), name='comment_detail'),
    path("<int:meetup_id>/questions/<question_id>/comments/<int:pk>/toggle_answer",
         ToggleAnswer.as_view(), name='toggle_answer'),
]
