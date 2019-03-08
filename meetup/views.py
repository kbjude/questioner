from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meeting
from .serializers import MeetingSerializer


# list all meetup or create a new meetup
# meetups/
class MeetingList(APIView):
    # permission_classes = (IsAuthenticated,)

    @classmethod
    def get(self, request):
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)
        return Response(serializer.data)

    @classmethod
    def post(self, request):
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
        serializer = MeetingSerializer(meetup, many=False)
        return Response(serializer.data)

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
