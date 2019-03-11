from django.contrib.auth.models import User
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(null=False)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)


class MeetingTag(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
