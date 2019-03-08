from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.IntegerField()
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()
    def __str__(self):
        return (self.title, self.body)

