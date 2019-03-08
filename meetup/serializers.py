from rest_framework import serializers

from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        # fields = ('title', 'date', 'start', 'end', 'created_by')
        fields = '__all__'
