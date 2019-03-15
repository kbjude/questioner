from rest_framework import serializers

from .models import Meeting
from .models import MeetingTag
from .models import Tag


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTag

        validators = [
            serializers.UniqueTogetherValidator(
                queryset = model.objects.all(),
                fields = ('tag', 'meetup'),
                message = ("Tag already exists on meet up.")
            )
        ]

        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
