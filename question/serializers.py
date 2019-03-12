from rest_framework import serializers
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
    class Meta:
        model = Question
        fields = "__all__"

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'
