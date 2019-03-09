from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(null=False)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
