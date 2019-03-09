from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meeting
from .models import MeetingTag
from .models import Tag
from .serializers import MeetingSerializer
from .serializers import UserSerializer
from .serializers import MeetingTagSerializer
from .serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated


class SignUp(APIView):
    """
    Register a user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'data': [{'user_id': user.pk,
                              'username': user.username,
                              'email': user.email,
                              'is_admin': user.is_superuser
                              }]
                })
        else:
            return Response({
                'status': 400,
                'errors': serializer.errors
            })


class Login(ObtainAuthToken):
    """
    login a user.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': 200,
            'token': token.key,
            'data': [{'user_id': user.pk,
                      'email': user.email
                      }]
        })
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)
        return Response(serializer.data)


# list all meetup or create a new meetup
# meetups/


class MeetingList(APIView):
    # permission_classes = (IsAuthenticated,)

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

        return Response(meetupwithtags)

    @classmethod
    def post(cls, request):

        data = request.data
        # data["created_at"] = str(datetime.datetime.now())

        serializer = MeetingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get, update or delete a meetup
# meetups/1
class AMeeting(APIView):

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

        return Response({"status":200, "data":result})

    @classmethod
    def put(cls, request, meeting_id):
        meetup = get_object_or_404(Meeting, pk=meeting_id)
        serializer = MeetingSerializer(meetup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request, meeting_id):
        meetup = get_object_or_404(Meeting, pk=meeting_id)
        meetup.delete()
        return Response({"successfully deleted"}, status=status.HTTP_200_OK)


# list all tags or create a tag
# tags/
class TagList(APIView):

    @classmethod
    def get(cls, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @classmethod
    def post(cls, request):

        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete a tag object
# tags/1
class ATag(APIView):

    @classmethod
    def delete(cls, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id)
        tag.delete()
        return Response({"successfully deleted"}, status=status.HTTP_200_OK)


# remove tag from meetup object
# meetups/1/tags/1
class AmeetupTag(APIView):

    @classmethod
    def delete(cls, request, tag_id, meeting_id):

        meetingtags = MeetingTag.objects.filter(meeting=meeting_id, tag=tag_id)
        serial_tags = MeetingTagSerializer(meetingtags, many=True)

        meetingtagid = serial_tags.data[0]['id']

        meetingtag = get_object_or_404(MeetingTag, pk=meetingtagid)
        meetingtag.delete()
        return Response({"successfully deleted"}, status=status.HTTP_200_OK)


# Add a tag to a meetup
# /meetups/tags/
class AddMeetupTag(APIView):

    @classmethod
    def post(cls, request):

        serializer = MeetingTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
