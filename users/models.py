from django.db import models

#Create your models here.
class QuestionerUsers(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(editable=False)

    def __str__(self):
        # return self.title, self.date, self.start, self.end, self.created_by
        return self.username