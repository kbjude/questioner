from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from question.models import Question
from question.serializers import QuestionSerializer


class Questions(APIView):
    """
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(self, request, meetup_id):
        """
            method is for getting all questions of a meeting
        """
        questions = Question.objects.filter(meetup_id=meetup_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @classmethod
    def post(self, request, meetup_id):
        """
            method is for adding a new question to a meeting
        """
        current_user = request.user
        if current_user.is_superuser:
            return Response(
                data={
                    "error": "Admin is not allowed to add questions",
                    "status": 401
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = request.data
        data["meetup_id"] = meetup_id
        data["created_by"] = current_user.id

        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={

                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {

                            "question": serializer.data,
                            "success": "Question successfully added to meetup"

                        }
                    ],
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OneQuestion(APIView):
    """
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, meetup_id, question_id):
        question = get_object_or_404(
            Question, id=question_id, meetup_id=meetup_id
        )
        serializer = QuestionSerializer(question, many=False)
        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {

                        "question": serializer.data,

                    }
                ],
            },
            status=status.HTTP_200_OK
        )

    @classmethod
    def put(cls, request, meetup_id, question_id):
        current_user = request.user
        if current_user.is_superuser:
            return Response(
                data={
                    "error": "Admin is not allowed to update a question",
                    "status": 401
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = request.data
        data["meetup_id"] = meetup_id
        data["created_by"] = current_user.id
        data["date_modified"] = timezone.now()
        question = get_object_or_404(
            Question, id=question_id, meetup_id=meetup_id, delete_status=False
        )
        serializer = QuestionSerializer(question, data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={

                    "status": status.HTTP_200_OK,
                    "data": [
                        {

                            "question": serializer.data,
                            "success": "Question successfully edited"

                        }
                    ],
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request, meetup_id, question_id):
        question = get_object_or_404(
            Question, id=question_id, meetup_id=meetup_id, delete_status=False
        )
        current_user = request.user
        if current_user.is_superuser:
            question.delete_status = True
            question.save()
            return Response(
                data={

                    "status": status.HTTP_200_OK,
                    "data": [
                        {
                            "success": "Question has been soft deleted",
                            "status": status.HTTP_200_OK,
                        }
                    ],
                },
                status=status.HTTP_200_OK
            )
        elif str(question.created_by) != str(current_user.username):
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "You cannot delete question created by another user"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            question.delete()
            return Response(
                data={

                    "status": status.HTTP_200_OK,
                    "data": [
                        {
                            "success": "Question has been deleted",
                        }
                    ],
                },
                status=status.HTTP_200_OK
            )
