from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from meetup.models import Meeting
from question.models import Question
from question.serializers import QuestionSerializer
from meetup.serializers import UserSerializer

class Questions(APIView):
    '''
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    '''
    # permission_classes = (IsAuthenticated,)

    @classmethod
    def get(self, request, meetup_id):
        '''
            method is for getting all questions of a meeting
        '''
        if Meeting.objects.filter(id=meetup_id):
            questions = Question.objects.filter(meetup_id=meetup_id)
            serializer = QuestionSerializer(questions, many=True)
            results = serializer.data
            all_questions = []
            for result in results:
                votes = [{'up votes': 0, 'down votes': 0}]
                result['votes'] = votes
                all_questions.append(result)
            return Response(all_questions)
        return Response({'error': 'invalid meetup id'}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def post(self, request, meetup_id):
        '''
            method is for adding a new question to a meeting
        '''
        if Meeting.objects.filter(id=meetup_id):
            data = request.data
            data['meetup_id'] = meetup_id
            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                votes = [{'up votes': 0, 'down votes': 0}]
                result = serializer.data
                result['votes'] = votes
                return Response(result, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'invalid meetup id'}, status=status.HTTP_400_BAD_REQUEST)

class OneQuestion(APIView):
    '''
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    '''
    @classmethod
    def get(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            question = get_object_or_404(Question, id=question_id, meetup_id=meetup_id)
            serializer = QuestionSerializer(question, many=False)
            votes = [{'up votes': 0, 'down votes': 0}]
            result = serializer.data
            result['votes'] = votes
            return Response(result)
        return Response({'error': 'invalid meetup id'}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def put(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            data = request.data
            data['meetup_id'] = meetup_id
            data['date_modified'] = timezone.now()
            question = get_object_or_404(Question, id=question_id, meetup_id=meetup_id)
            serializer = QuestionSerializer(question, data)
            if serializer.is_valid():
                serializer.save()
                votes = [{'up votes': 0, 'down votes': 0}]
                result = serializer.data
                result['votes'] = votes
                return Response(result)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'invalid meetup id'}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            question = get_object_or_404(Question, id=question_id, meetup_id=meetup_id)
            question.delete()
            return Response({"successfully deleted"}, status=status.HTTP_200_OK)
        return Response({'error': 'invalid meetup id'}, status=status.HTTP_400_BAD_REQUEST)
        