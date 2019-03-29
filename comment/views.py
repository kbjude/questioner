from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from meetup.models import Meeting
from question.models import Question
from .models import Comment
from .serializers import CommentSerializer, ReactionSerializer


class CommentList(APIView):
    """
    List all comments, or create a new comment.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get(self, request, **kwargs):
        """Return a list of comments."""
        meetup = Meeting.objects.filter(id=self.kwargs['meetup_id'])
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if meetup:
            if not question:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "Question not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            queryset = Comment.objects.filter(question=self.kwargs['question_id'])
            serializer = CommentSerializer(queryset, many=True)

            data = []
            for comment in serializer.data:
                user = User.objects.filter(Q(username=comment["created_by"])).distinct().first()
                comment["created_by_id"] = user.id
                comment["question_name"] = question.first().title
                data.append(comment)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comments": data
                }
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request, **kwargs):
        """Add a comment to a particular question."""
        meetup = Meeting.objects.filter(id=self.kwargs['meetup_id'])
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if meetup:
            if not question:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "Question not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            data = {}
            data["question"] = question.first().id
            data["comment"] = request.data.get("comment")

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    created_by_id=request.user.id,
                    created_by=self.request.user,
                    question_id=self.kwargs['question_id']
                )
                data = dict(serializer.data)
                data["created_by_id"] = request.user.id
                data["question_name"] = question.first().title
                return Response(
                    {
                        "comment": serializer.data,
                        "message": "Comment successfully created."
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": "Fields cannot be left empty or missing."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


class ToggleAnswer(APIView):
    """
    Turn a comment into an answer
    Or tun an answer into a comment
    Only the admin has rights to this endpoint
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwags):

        try:
            question_id = self.kwargs['question_id']
            comment_id = self.kwargs['pk']

            if request.user.is_superuser:
                comment = Comment.objects.get(id=comment_id,
                                              question=question_id
                                              )

                serializer = CommentSerializer(comment, many=False)

                data = dict(serializer.data)
                data["is_answer"] = not data["is_answer"]

                serializer = CommentSerializer(comment, data=data,
                                               partial=True
                                               )
                if serializer.is_valid():
                    serializer.save(is_answer=True)
                    return Response(
                                {
                                    "status": status.HTTP_200_OK,
                                    "message": "Comment successfully updated."
                                }
                                    )
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "error": "Insurfficient rights."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        except Comment.DoesNotExist:
            return Response(
                data={
                    "status": 404,
                    "error": "Meetup or question does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment instance.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    @classmethod
    def get_object(cls, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound({"error": "Comment not found."})

    def get(self, request, pk, **kwargs):
        """Return a single comment to a question."""
        if not Meeting.objects.filter(id=self.kwargs['meetup_id']):
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Meetup not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if not question:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if Comment.objects.filter(question=self.kwargs['question_id']):
            comment = self.get_object(pk)
            serializer = CommentSerializer(comment)

            data = dict(serializer.data)
            user = User.objects.filter(Q(username=data["created_by"])).distinct().first()
            print(user)
            data["created_by_id"] = user.id
            data["question_name"] = question.first().title
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comment": data
                }
            )

    def put(self, request, pk, **kwargs):
        """Update a single comment."""
        if Meeting.objects.filter(id=self.kwargs['meetup_id']):
            if Question.objects.filter(id=self.kwargs['question_id']):
                if Comment.objects.filter(question=self.kwargs['question_id']):
                    comment = self.get_object(pk)
                    comment_owner = comment.created_by
                    if comment_owner == request.user:
                        serializer = CommentSerializer(comment, many=False)
                        data = dict(serializer.data)
                        data["comment"] = request.data["comment"]

                        serializer = CommentSerializer(comment, data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(
                                {
                                    "status": status.HTTP_200_OK,
                                    "message": "Comment successfully updated."
                                }
                            )
                    return Response(
                        {
                            "status": status.HTTP_403_FORBIDDEN,
                            "error": "You cannot update this comment."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, pk, **kwargs):
        """Delete a single question."""
        if Meeting.objects.filter(id=self.kwargs['meetup_id']):
            if Question.objects.filter(id=self.kwargs['question_id']):
                if Comment.objects.filter(question=self.kwargs['question_id']):
                    comment = self.get_object(pk)
                    comment_owner = comment.created_by
                    if comment_owner == request.user:
                        comment.delete()
                        return Response(
                            {
                                "status": status.HTTP_204_NO_CONTENT,
                                "message": "Comment successfully deleted."
                            },
                            status=status.HTTP_204_NO_CONTENT
                        )
                    return Response(
                        {
                            "status": status.HTTP_403_FORBIDDEN,
                            "error": 'You cannot delete this comment.'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

# Add a reaction
class AddReaction(APIView):
    """
    post: reaction
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ReactionSerializer

    @classmethod
    # @swagger_auto_schema(
    #     operation_description="Add a tag to a meetup",
    #     operation_id="Add a tag to a meetup.",
    #     request_body=MeetingTagSerializer,
    #     responses={
    #         201: MeetingTagSerializer(many=False),
    #         401: "Unathorized Access",
    #         403: "Tag is disabled",
    #         404: "Tag Does not exist",
    #         400: "Meet up does not exist or Tag already exists",
    #     },
    # )
    def post(cls, request, comment_id):

        data = {}
        data["comment_id"] = comment_id
        data["reaction"] = request.data["reaction"]

        try:
            comment = Comment.objects.get(pk=data["comment_id"])
            serializer = ReactionSerializer(data=data)

        except Exception:
            return Response(
                data={
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Comment does not exist!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        response = None
        if not comment.is_answer:
            response = Response(
                data={
                    "status": status.HTTP_403_FORBIDDEN,
                    "error": "Sorry, reactions can only be made on answers.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        elif serializer.is_valid():
            serializer.save(comment_id=comment_id)

            response = Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "success": "Reaction successfully added.",
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            response = Response(
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response
