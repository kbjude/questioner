from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from meetup.models import Meeting
from question.models import Question, Vote
from question.serializers import QuestionSerializer, VoteSerializer


class Questions(APIView):
    """
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    @swagger_auto_schema(
        operation_description="Get all Questions for a meet up",
        operation_id="Get all questions for a meetup",
        responses={
            200: QuestionSerializer(many=True),
            400: "Invalid Meetup Id",
        },
    )
    def get(self, request, meetup_id):
        """
        get:
        Get all Questions for a meet up
        """
        if Meeting.objects.filter(id=meetup_id):
            questions = Question.objects.filter(meetup_id=meetup_id)
            serializer = QuestionSerializer(questions, many=True)
            results = serializer.data
            all_questions = []
            for result in results:
                up_votes = len(
                    [
                        vote
                        for vote in Vote.objects.filter(
                            question_id=result["id"], vote=1
                        )
                    ]
                )
                dwn_votes = len(
                    [
                        vote
                        for vote in Vote.objects.filter(
                            question_id=result["id"], vote=-1
                        )
                    ]
                )
                votes = [{"up votes": up_votes, "down votes": dwn_votes}]
                result["votes"] = votes
                all_questions.append(result)
            return Response(all_questions)
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a question for a specific meetup.",
        operation_id="Create a question for a specific meetup",
        request_body=QuestionSerializer,
        responses={
            201: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def post(self, request, meetup_id):
        """
        post:
        Create a question for a specific meetup."
        """
        if Meeting.objects.filter(id=meetup_id):
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to add questions",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
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
                                "success": "Question successfully added to meetup",
                            }
                        ],
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )


class OneQuestion(APIView):
    """
    get:
    Get a question for a specific meetup."
    put:
    Update a question for a specific meetup."
    delete:
    Delete a question for a specific meetup."
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    @swagger_auto_schema(
        operation_description="Get a question for a specific meetup.",
        operation_id="Get a question for a specific meetup.",
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def get(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            question = get_object_or_404(
                Question, id=question_id, meetup_id=meetup_id
            )
            serializer = QuestionSerializer(question, many=False)
            result = serializer.data
            up_votes = len(
                [
                    votes
                    for votes in Vote.objects.filter(
                        question_id_id=result["id"], vote=1
                    )
                ]
            )
            dwn_votes = len(
                [
                    votes
                    for votes in Vote.objects.filter(
                        question_id=result["id"], vote=-1
                    )
                ]
            )
            votes = [{"up votes": up_votes, "down votes": dwn_votes}]
            result["votes"] = votes
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [{"question": result}],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Update a question for a specific meetup.",
        operation_id="Update a question for a specific meetup.",
        request_body=QuestionSerializer,
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def put(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to update a question",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            data = request.data
            data["meetup_id"] = meetup_id
            data["created_by"] = current_user.id
            data["date_modified"] = timezone.now()
            question = get_object_or_404(
                Question,
                id=question_id,
                meetup_id=meetup_id,
                delete_status=False,
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
                                "success": "Question successfully edited",
                            }
                        ],
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Delete a question for a specific meetup.",
        operation_id="Delete a question for a specific meetup.",
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Meetup ID",
            404: "Invalid Question ID",
            401: "Unauthorized Access",
        },
    )
    def delete(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            question = get_object_or_404(
                Question,
                id=question_id,
                meetup_id=meetup_id,
                delete_status=False,
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
                    status=status.HTTP_200_OK,
                )
            elif str(question.created_by) != str(current_user.username):
                return Response(
                    data={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "You cannot delete question created by another user",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                question.delete()
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [{"success": "Question has been deleted"}],
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

class UpVote(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    @swagger_auto_schema(
        operation_description="Upvote or Down vote",
        operation_id="Upvote or Down vote on a Question",
        request_body=VoteSerializer,
        responses={
            201: VoteSerializer(many=False),
            401: "Unathorized Access",
            400: "Bad Request",
        },
    )
    def post(self, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user
                data = request.data
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                data['vote'] = 1
                serializer = VoteSerializer(data=data)
                if not Question.objects.filter(id=question_id, created_by=current_user.id):
                    my_vote = Vote.objects.filter(question_id=question_id, voter_id=current_user.id)
                    my_vote_is_up = Vote.objects.filter(question_id=question_id, voter_id=current_user.id, vote=1)
                    if my_vote:
                        if my_vote_is_up:
                            my_vote.delete()
                            return Response(
                                data={
                                    "status": status.HTTP_200_OK,
                                    "data": [{"success": "your up-vote has been cancelled"}],
                                    },
                                    status=status.HTTP_200_OK,
                            )
                        my_vote = get_object_or_404(Vote, question_id=question_id, voter_id=current_user.id, vote=-1)
                        serializer = VoteSerializer(my_vote, data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            data={
                                "status": status.HTTP_201_CREATED,
                                "data": [
                                    {
                                        "vote": serializer.data,
                                        "success": "you have up-voted this question",
                                    }
                                ],
                            },
                            status=status.HTTP_201_CREATED,
                        )
                return Response(
                    {
                        "error": "vote rejected",
                        "message": "question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class DownVote(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(self, request, meetup_id, question_id):
    @swagger_auto_schema(
        operation_description="Update vote",
        operation_id="Update vote on a question.",
        request_body=VoteSerializer,
        responses={
            200: VoteSerializer(many=False),
            401: "Unathorized Access",
            400: "Bad Request",
        },
    )
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user
                data = request.data
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                data['vote'] = -1
                serializer = VoteSerializer(data=data)
                if not Question.objects.filter(id=question_id, created_by=current_user.id):
                    my_vote = Vote.objects.filter(question_id=question_id, voter_id=current_user.id)
                    my_vote_is_down = Vote.objects.filter(question_id=question_id, voter_id=current_user.id, vote=-1)
                    if my_vote:
                        if my_vote_is_down:
                            my_vote.delete()
                            return Response(
                                data={
                                    "status": status.HTTP_200_OK,
                                    "data": [{"success": "your up-vote has been cancelled"}],
                                    },
                                    status=status.HTTP_200_OK,
                            )
                        my_vote = get_object_or_404(Vote, question_id=question_id, voter_id=current_user.id, vote=1)
                        serializer = VoteSerializer(my_vote, data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            data={
                                "status": status.HTTP_201_CREATED,
                                "data": [
                                    {
                                        "vote": serializer.data,
                                        "success": "you have up-voted this question",
                                    }
                                ],
                            },
                            status=status.HTTP_201_CREATED,
                        )
                return Response(
                    {
                        "error": "vote rejected",
                        "message": "question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
