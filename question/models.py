from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now_add=True)
    meetup_id = models.IntegerField()
    delete_status = models.BooleanField(default=False)
    def __str__(self):
        return (self.title, self.body) # pragma: no cover
    


