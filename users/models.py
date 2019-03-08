from django.db import models

#Create your models here.
class QuestionerUsers(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    is_admin = models.BooleanField()

    def __str__(self):
        # return self.title, self.date, self.start, self.end, self.created_by
        return self.username