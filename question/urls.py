# from django.urls import path, include
# from . import views


# urlpatterns = [
#     path('auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('', views.QuestionList.as_view()),
#     path('<question_id>', views.question)
# ]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import QuestionsView, QuestionDetails, CommentsView, CommentDetails


urlpatterns = {
    url(r'^questions/$', QuestionsView.as_view(),
        name='question_view'),
    url(r'^questions/(?P<pk>[0-9]+)/$', QuestionDetails.as_view(),
        name='question_details'),
    url(r'^questions/(?P<pk>[0-9]+)/comments/$', CommentsView.as_view(),
        name='comment_view'),
    url(r'^questions/(?P<pk>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$',
        CommentDetails.as_view(), name='comment_view')
}

urlpatterns = format_suffix_patterns(urlpatterns)
