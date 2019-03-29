from django.db import models
from django.contrib.auth.models import User
from question.models import Question


class Comment(models.Model):
    """This class represents the comment model."""

    question = models.ForeignKey(Question, related_name='comments',
                                 on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(User, related_name='comments',
                                   on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        """Return a readable representation of the comment model instance."""
        return self.comment


class Reaction(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING,
                                related_name='reactions')
    reaction = models.TextField()

    def __str__(self):
        return (self.reaction, self.comment,)
