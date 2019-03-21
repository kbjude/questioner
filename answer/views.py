from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Answers
from question.models import Question
from answer.serializers import AnswerSerializer
class CreateReadAnswers(APIView):
    """
    post:
    Create an answer to a specific question
    get:
    Get answers to a specific question
    put:
    Edit an answer to a specific question
    delete:
    Delete an answer to a specific question
    """

    permission_classes = (IsAuthenticated,)


    def post(self, request, meetup_id, question_id, format=None):
        """
        Creates an answer for a specific question.
        Only staff can answer a question
        """
        active_user = request.user
        if not active_user.is_staff:
            return Response(
                data = {
                "status": 401,
                "error": "Only staff are allowed to answer questions"
                },
                status = status.HTTP_401_UNAUTHORIZED
            )
        response = None
        try:
            question = Question.objects.get(id=question_id, meetup_id=meetup_id)
            data  = request.data
            data['created_by'] = request.user.id
            data['question'] = question_id
            data['meetup'] = meetup_id
            serializer = AnswerSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                response = Response(
                    data = {
                        "status": 201,
                        "data":[{
                            "answer": serializer.data,
                            "success": "Answer added successfully"

                        }],
                    },
                    status = status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    data = {
                        "status": 400,
                        "error":serializer.errors,
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

        except Question.DoesNotExist:

            response = Response(
                data ={
                    "status": 404,
                    "error": "Meetup or question does not exist"
                },
                status = status.HTTP_404_NOT_FOUND
            )
        return response
