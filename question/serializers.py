from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from question.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'

