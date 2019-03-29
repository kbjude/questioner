from rest_framework import serializers
from .models import Comment, Reaction


class ReactionsField(serializers.RelatedField):
    @classmethod
    def to_representation(cls, value, queryset=Reaction.objects.all()):
        return value.reaction


class CommentSerializer(serializers.ModelSerializer):
    """Map the comment model instance into JSON format."""

    reactions = ReactionsField(many=True, read_only=True)

    created_by = serializers.ReadOnlyField(source='created_by.username')
    # question_name = serializers.ReadOnlyField(source='question.title')

    class Meta:
        """Map serializer fields to comment model fields."""
        model = Comment
        fields = "__all__"
        read_only_fields = ("is_answer", "question", )


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        read_only_fields = ("comment",)
