from rest_framework import serializers

from .models import Meeting
from .models import MeetingTag
from .models import Tag


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        # fields = ('title', 'date', 'start', 'end', 'created_by')


class MeetingTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTag
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
