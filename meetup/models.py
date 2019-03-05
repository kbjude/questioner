from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField()
    created_by = models.IntegerField()

    def __str__(self):
        # return self.title, self.date, self.start, self.end, self.created_by
        return self.title
