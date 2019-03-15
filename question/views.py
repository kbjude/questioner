from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from meetup.models import Meeting
from question.models import Question, Vote
from question.serializers import QuestionSerializer, VoteSerializer
from meetup.serializers import MeetingSerializer


class Questions(APIView):
    """
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    @classmethod
    def get(self, request, meetup_id, *args, **kwargs):
        """
            method is for getting all questions of a meeting
        """

        mymeeting = Meeting.objects.filter(id=meetup_id)
        if mymeeting.exists():
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

                Mserializer = MeetingSerializer(mymeeting, many=True)

                resultdata={}
                resultdata["Id"] = result["id"]
                resultdata["Title"] = result["title"]
                resultdata["Body"] = result["body"]
                resultdata["Meetup"] = Mserializer.data[0]["title"]
                resultdata["Deleted"] = result["delete_status"]
                resultdata["Created By"] = request.user.username
                resultdata["Created On"] = result["date_created"]
                resultdata["Last Updated on"] = result["date_modified"]
                resultdata["votes"] = votes

                all_questions.append(resultdata)
            return Response(all_questions)
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def post(self, request, meetup_id):
        """
            method is for adding a new question to a meeting
        """

        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to add questions",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            data={}
            data["title"] = request.data.get("title", None)
            data["body"] = request.data.get("body", None)
            data["meetup_id"] = meetup_id
            data["created_by"] = current_user.id

            Mserializer = MeetingSerializer(meeting, many=True)

            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():

                serializer.save()
                qn_dict = dict(serializer.data)
                qn_dict["created_by"] = current_user.username
                qn_dict["meetup_id"] = Mserializer.data[0]["title"]
                return Response(
                    data={
                        "status": status.HTTP_201_CREATED,
                        "data": [
                            {
                                "question": qn_dict,
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
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    @classmethod
    def get(cls, request, meetup_id, question_id):

        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
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

            Mserializer = MeetingSerializer(meeting, many=True)

            resultdata={}
            resultdata["Id"] = result["id"]
            resultdata["Title"] = result["title"]
            resultdata["Body"] = result["body"]
            resultdata["Meetup"] = Mserializer.data[0]["title"]
            resultdata["Deleted"] = result["delete_status"]
            resultdata["Created By"] = request.user.username
            resultdata["Created On"] = result["date_created"]
            resultdata["Last Updated on"] = result["date_modified"]
            resultdata["votes"] = votes
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [{"question": resultdata}],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def put(cls, request, meetup_id, question_id):
        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to update a question",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            question = get_object_or_404(
                Question,
                id=question_id,
                meetup_id=meetup_id,
                delete_status=False,
            )
            serializer = QuestionSerializer(question, many=False)

            data=dict(serializer.data)
            data["title"] = request.data.get("title", None)
            data["body"] = request.data.get("body", None)
            # data["meetup_id"] = meetup_id
            # data["created_by"] = current_user.id
            data["date_modified"] = timezone.now()

            serializer = QuestionSerializer(question, data)
            if serializer.is_valid():
                serializer.save()

                Mserializer = MeetingSerializer(meeting, many=True)
                
                qn_dict = dict(serializer.data)
                qn_dict["created_by"] = current_user.username
                qn_dict["meetup_id"] = Mserializer.data[0]["title"]
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [
                            {
                                "question": qn_dict,
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


class Votes(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = VoteSerializer

    @classmethod
    def post(self, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user

                data={}
                data["vote"] = request.data.get("vote", None)
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                serializer = VoteSerializer(data=data)
                voter_check_1 = Question.objects.filter(
                    id=question_id, created_by=current_user.id
                )
                voter_check_2 = Vote.objects.filter(
                    question_id=question_id, voter_id=current_user.id
                )
                if not voter_check_1 and not voter_check_2:
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            data={
                                "status": status.HTTP_201_CREATED,
                                "data": [
                                    {
                                        "success": "Vote successfully added to question",
                                    }
                                ],
                            },
                            status=status.HTTP_201_CREATED,
                        )
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "error": "vote rejected",
                        "message": "either you already voted or question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @classmethod
    def put(self, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user
                data = request.data
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                voter_check_1 = Question.objects.filter(
                    id=question_id, created_by=current_user.id
                )
                voter_check_2 = Vote.objects.filter(
                    question_id=question_id, voter_id=current_user.id
                )
                if not voter_check_1 and voter_check_2:
                    vote = get_object_or_404(
                        Vote, question_id=question_id, voter_id=current_user.id
                    )
                    serializer = VoteSerializer(vote, data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            data={
                                "status": status.HTTP_200_OK,
                                "data": [
                                    {
                                        "success": "Vote successfully edited",
                                    }
                                ],
                            },
                            status=status.HTTP_200_OK,
                        )
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        "error": "vote edit rejected",
                        "message": "either you have not voted yet or question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
