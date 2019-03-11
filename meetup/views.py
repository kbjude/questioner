import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

    @classmethod
    def get(cls, request):
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)

        meetupwithtags = []
        for meetup in serializer.data:

            meetingtags = MeetingTag.objects.filter(meeting=meetup['id'])
            serial_tags = MeetingTagSerializer(meetingtags, many=True)

            meetuptags = []
            for meetuptag in serial_tags.data:
                tag = Tag.objects.get(id=meetuptag['tag'])
                meetuptags.append(tag.title)

            meetup["tags"] = meetuptags
            meetupwithtags.append(meetup)

        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {

                        "meetup": meetupwithtags,
                    }
                ],
            },
            status=status.HTTP_200_OK
        )

    @classmethod
    def post(cls, request):

        if not request.user.is_superuser:
            return Response(
                data={

                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error":  "Action restricted to Admins!"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


        data = request.data
        data["created_by"] = request.user.id
        data["created_at"] = str(datetime.datetime.now())

        serializer = MeetingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={

                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {

                            "meetup": serializer.data,
                            "success": "Meet up created successfully"

                        }
                    ],
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={

                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# Get, update or delete a meetup
# meetups/1
class AMeeting(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, meeting_id):

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        serial_meeting = MeetingSerializer(meetup, many=False)

        meetingtags = MeetingTag.objects.filter(meeting=meeting_id)
        serial_tags = MeetingTagSerializer(meetingtags, many=True)

        tags = []
        for item in serial_tags.data:
            tag = Tag.objects.get(id=item['tag'])
            tags.append(tag.title)

        result = serial_meeting.data
        result["tags"] = tags

        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {

                        "meetup": result,

                    }
                ],
            },
            status=status.HTTP_200_OK
        )

    @classmethod
    def put(cls, request, meeting_id):

        if not request.user.is_superuser:

            return Response(
                data={

                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error":  "Action restricted to Admins!"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


        meetup = get_object_or_404(Meeting, pk=meeting_id)
        data = request.data
        data["created_by"] = request.user.id


        serializer = MeetingSerializer(meetup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={

                    "status": status.HTTP_200_OK,
                    "data": [
                        {

                            "meetup": serializer.data,
                            "success": "Meet updated successfully"

                        }
                    ],
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={

                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    @classmethod
    def delete(cls, request, meeting_id):

        if not request.user.is_superuser:
            return Response(
                data={

                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error":  "Action restricted to Admins!"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        meetup.delete()

        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {
                        "success": "Meet deleted successfully"

                    }
                ],
            },
            status=status.HTTP_200_OK
        )

# list all tags or create a tag
# tags/
class TagList(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @classmethod
    def post(cls, request):

        if not request.user.is_superuser:
            return Response({"message": "Action restricted to Admins!", "status": 401},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        data["created_by"] = request.user.id

        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a tag object
# tags/1
class ATag(APIView):
    permission_classes = (IsAdminUser,)

    @classmethod
    def delete(cls, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id)
        serial_tag = TagSerializer(tag, many=False)

        data = serial_tag.data
        data["active"] = False

        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"successfully deleted"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# remove tag from meetup object
# meetups/1/tags/1
class AmeetupTag(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def delete(cls, request, tag_id, meeting_id):
        meetingtags = MeetingTag.objects.filter(meeting=meeting_id, tag=tag_id)
        serial_tags = MeetingTagSerializer(meetingtags, many=True)
        serial_tag = serial_tags.data[0]

        if not (request.user.is_superuser or (request.user.id == serial_tag["created_by"])):
            return Response({"message": "Sorry. Permission denied!", "status": 401},
                            status=status.HTTP_401_UNAUTHORIZED)

        meetingtagid = serial_tags.data[0]['id']

        meetingtag = get_object_or_404(MeetingTag, pk=meetingtagid)
        meetingtag.delete()
        return Response({"successfully deleted"}, status=status.HTTP_200_OK)


# Add a tag to a meetup
# /meetups/tags/
class AddMeetupTag(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request):

        data = request.data
        data["created_by"] = request.user.id

        tag = get_object_or_404(Tag, pk=data["tag"])
        serial_tag = TagSerializer(tag, many=False)
        if not serial_tag.data["active"]:
            return Response({"message": "This Tag is disabled", "status": 403}, status=status.HTTP_403_FORBIDDEN)

        serializer = MeetingTagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
