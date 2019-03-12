from rest_framework import serializers
from django.contrib.auth.models import User
from question.models import Question, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Map the comment model instance into JSON format."""

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        """Map serializer fields to comment model fields."""
        model = Comment
        fields = ('id', 'comment', 'created_by', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class QuestionSerializer(serializers.ModelSerializer):
    
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'body', 'created_by', 'date_created', 
                  'date_modified', 'comments')
        read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    """Serializer to aid in Authentication and Authorization."""

    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all())

    class Meta:
        """Map serializer fields to the user."""
        model = User
        fields = ('id', 'username', 'questions')


# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'
