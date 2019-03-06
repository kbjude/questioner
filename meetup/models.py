from django.db import models
from rest_framework import authentication


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


class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'
