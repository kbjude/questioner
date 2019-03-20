from django.contrib.auth.models import User
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(null = True)
    date = models.DateField(null=False)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return (self.title)


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (self.title)


class MeetingTag(models.Model):
    meetup = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("tag", "meetup")

    def __str__(self):
        return (self.tag)
