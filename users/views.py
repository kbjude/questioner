from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from users.models import QuestionerUsers

@csrf_exempt
def user_signup(request):
    '''
        this views method is responsible for the following;
        - creating new users, user signup
        - getting all users from the database
    '''
    if request.method == 'POST':
        payload = json.loads(request.body)
        firstname = payload['firstname']
        lastname = payload['lastname']
        username = payload['username']
        password = payload['password']
        email = payload['email']
        phonenumber = payload['phonenumber']

        user = QuestionerUsers(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phonenumber, date_created = timezone.now())
        try:
            user.save()
            response = json.dumps([{'message': 'user successfully registered'}]),201          
            
        except:
            response = json.dumps([{'error': 'user could not be registered'}]),400
