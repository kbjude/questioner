from django.urls import path

from . import views

urlpatterns = [
    path('', views.questions),
    path('<question_id>', views.question)
]
