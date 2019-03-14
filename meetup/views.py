import datetime

from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meeting
from .models import MeetingTag
from .models import Tag
from .serializers import MeetingSerializer
from .serializers import MeetingTagSerializer
from .serializers import TagSerializer


# list all meetup or create a new meetup
# meetups/
class MeetingList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingSerializer

    @classmethod
    def get(cls, request):
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)

        meetupwithtags = []
        for meetup in serializer.data:

            meetingtags = MeetingTag.objects.filter(meetup=meetup["id"])
            serial_tags = MeetingTagSerializer(meetingtags, many=True)

            meetuptags = []
            for meetuptag in serial_tags.data:
                tag = Tag.objects.get(id=meetuptag["tag"])
                meetuptags.append(tag.title)

            meetup["tags"] = meetuptags
            meetupwithtags.append(meetup)

        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"meetup": meetupwithtags}],
            },
            status=status.HTTP_200_OK,
        )

    @classmethod
    def post(cls, request):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = {}
        data["created_by"] = request.user.id
        data["title"] = request.data["title"]
        data["date"] = request.data["date"]
        data["start"] = request.data["start"]
        data["end"] = request.data["end"]

        serializer = MeetingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "meetup": serializer.data,
                            "success": "Meet up created successfully",
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Get, update or delete a meetup
# meetups/1
class AMeeting(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingSerializer

    @classmethod
    def get(cls, request, meeting_id):

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        serial_meeting = MeetingSerializer(meetup, many=False)

        meetingtags = MeetingTag.objects.filter(meetup=meeting_id)
        serial_tags = MeetingTagSerializer(meetingtags, many=True)

        tags = []
        for item in serial_tags.data:
            tag = Tag.objects.get(id=item["tag"])
            tags.append(tag.title)

        result = serial_meeting.data
        result["tags"] = tags

        return Response(
            data={"status": status.HTTP_200_OK, "data": [{"meetup": result}]},
            status=status.HTTP_200_OK,
        )

    @classmethod
    def put(cls, request, meeting_id):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetup = get_object_or_404(Meeting, pk=meeting_id)

        serializer = MeetingSerializer(meetup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [
                        {
                            "meetup": serializer.data,
                            "success": "Meet updated successfully",
                        }
                    ],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @classmethod
    def delete(cls, request, meeting_id):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        meetup.delete()

        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"success": "Meet deleted successfully"}],
            },
            status=status.HTTP_200_OK,
        )


# list all tags or create a tag
# tags/
class TagList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    @classmethod
    def get(cls, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"tags": serializer.data}],
            },
            status=status.HTTP_200_OK,
        )

    @classmethod
    def post(cls, request):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data={}
        data["title"] = request.data["title"]
        data["created_by"] = request.user.id

        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "tag": serializer.data,
                            "success": "Tag created successfully",
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# delete a tag object
# tags/1
class ATag(APIView):
    """
    delete:
    Delete a tag.
    """

    permission_classes = (IsAdminUser,)
    serializer_class = TagSerializer

    @classmethod
    def delete(cls, request, tag_id):
        """
        Delete a Tag
        """
        tag = get_object_or_404(Tag, pk=tag_id)
        response = None
        try:
            tag.delete()
            response = Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [
                        {"success": "Tag permantely deleted successfully"}
                    ],
                },
                status=status.HTTP_200_OK,
            )
        except ProtectedError:
            tag.is_active = False
            tag.save()
            response = Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [{"success": "Tag soft deleted successfully"}],
                },
                status=status.HTTP_200_OK,
            )
        return response


# Add a tag to a meetup
# /meetups/{meet_up_id}tags/
class AddMeetupTag(APIView):
    """
    put:
    A tag to a meet up
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingTagSerializer

    @classmethod
    def post(cls, request, meeting_id):


        data={}
        data["tag"] = request.data["tag"]
        data["created_by"] = request.user.id
        data["meetup"] = meeting_id
        try:
            tag = Tag.objects.get(pk=data["tag"])
            serializer = MeetingTagSerializer(data=data)

        except Tag.DoesNotExist:
            return Response(
                data={
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Tag with specified id does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        response = None

        if not tag.active:
            response = Response(
                data={
                    "status": status.HTTP_403_FORBIDDEN,
                    "error": "This Tag is disabled.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        elif serializer.is_valid():
            try:
                serializer.save()
                response = Response(
                    data={
                        "status": status.HTTP_201_CREATED,
                        "data": [
                            {
                                "tag": serializer.data,
                                "success": "Tag successfully added to meetup",
                            }
                        ],
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:

                response = Response(
                    data={
                        "status": status.HTTP_409_CONFLICT,
                        "error": "Tag already exists on meetup",
                    },
                    status=status.HTTP_409_CONFLICT,
                )
        else:
            response = Response(
                data={
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Meetup with specified id does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return response


# remove tag from meetup object
# meetups/1/tags/1
class AmeetupTag(APIView):
    """
    delete:
    Remove tag from meetup.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingTagSerializer

    @classmethod
    def delete(cls, request, tag_id, meeting_id):
        meetingtags = get_object_or_404(
            MeetingTag, meetup=meeting_id, tag=tag_id
        )
        serializer = MeetingTagSerializer(meetingtags, many=False)

        serial_tag = serializer.data

        if not (
            request.user.is_superuser
            or (request.user.id == serial_tag["created_by"])
        ):
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Sorry. Permission denied!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetingtags.delete()
        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [
                    {"success": "Tag successfully removed from Meet up."}
                ],
            },
            status=status.HTTP_200_OK,
        )
