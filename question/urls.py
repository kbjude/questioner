# from django.urls import path, include
# from . import views


# urlpatterns = [
#     path('auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('', views.QuestionList.as_view()),
#     path('<question_id>', views.question)
# ]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import QuestionView, QuestionDetails


urlpatterns = {
    url(r'^questions/$', QuestionView.as_view(), name='question_view'),
    url(r'^questions/(?P<pk>[0-9]+)/$', QuestionDetails.as_view(), name='question_details')
}

urlpatterns = format_suffix_patterns(urlpatterns)
