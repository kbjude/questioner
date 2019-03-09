from django.db import models

class Question(models.Model):
    """This class represents the question model."""

    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.ForeignKey('auth.User', related_name='questions',
                                   on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable representation of the question model instance."""
        return "{}".format(self.title)


class Comment(models.Model):
    """This class represents the comment model."""

    question = models.ForeignKey(Question, related_name='comments',
                                 on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey('auth.User', related_name='comments',
                                   on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable representation of the comment model instance."""
        return "{}".format(self.comment)
