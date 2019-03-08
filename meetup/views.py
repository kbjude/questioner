from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Meeting
from .serializers import MeetingSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status


# list all meetup or create a new meetup
# meetups/
class MeetingList(APIView):
    # permission_classes = (IsAuthenticated,)

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
