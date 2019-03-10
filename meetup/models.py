from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(null=False)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
                        'auth.User',
                        related_name='meeting',
                        on_delete=models.CASCADE)
