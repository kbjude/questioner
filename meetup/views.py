from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .models import Meeting
from .serializers import MeetingSerializer
from .serializers import UserSerializer


# list all meetup or create a new meetup
# meetups/
class Index(APIView):

    @classmethod
    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})


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
        serializer = self.serializer_class(data=request.data)
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


# list all meetup or create a new meetup
# meetups/


class MeetingList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = MeetingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# Get, update or delete a meetup
# meetups/1
class AMeeting(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, meeting_id):
        meetup = get_object_or_404(Meeting, pk=meeting_id)
        serializer = MeetingSerializer(meetup, many=False)
        return Response(serializer.data)

    def put(self, request, meeting_id):
        permission_classes = (IsOwnerOrReadOnly, )
        obj = get_object_or_404(Meeting, pk=meeting_id)
        serializer = MeetingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, meeting_id):
        meetup = get_object_or_404(Meeting, pk=meeting_id)
        meetup.delete()
        return Response({"successfully deleted"}, status=status.HTTP_200_OK)
