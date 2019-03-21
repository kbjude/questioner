from django.urls import path

from answer.views import CreateReadAnswers

urlpatterns = [
    path(
        "<int:meetup_id>/questions/<int:question_id>/answers/",
        CreateReadAnswers.as_view(),
        name="create_read_answers",
    ),
]
# format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)
