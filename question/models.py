from django.contrib.auth.models import User
from django.db import models

from meetup.models import Meeting


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now_add=True)
    meetup_id = models.ForeignKey(
        Meeting, on_delete=models.CASCADE)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return (self.title, self.body)  # pragma: no cover


class Vote(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    voter_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField()
    date_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.voter_id, self.vote)  # pragma: no cover


class Comment(models.Model):
    """This class represents the comment model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.comment)


class Mycomment(models.Model):
    comment = models.TextField()
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False

    def __str__(self):
        return (self.comment)
