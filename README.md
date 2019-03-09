# Questioner
by The dojos

[![Build Status](https://travis-ci.com/kbjude/questioner.svg?branch=develop)](https://travis-ci.com/kbjude/questioner)
[![Coverage Status](https://coveralls.io/repos/github/kbjude/questioner/badge.svg?branch=develop)](https://coveralls.io/github/kbjude/questioner?branch=develop)

## Introduction
Questioner is ...

## Installation
    - Clone this repository.

    - Setup a virtual environment and activate it.
from rest_framework import authentication

class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prependefrom rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prependefrom rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'd with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'd with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'
    - Install the requirements.txt

    - Add a ".env" file that has:

        - export DJANGO_SETTINGS_MODULE="questioner.settings"

        - export DATABASE_NAME

        - export DATABASE_HOST

        - export DATABASE_USER

        - export DATABASE_PASSWORD

 ## Running the application
  Open the directory of the application in the terminal and execute:

    python manage.py migrate
    python manage.py runserver

   In a browser type the Url: http//localhost:8000.

 ## Login
  Using postman login with endpoint: http//localhost:8000/auth/login
  Provide your credentials under the body tab
  {
  	"username": "your-username",
	  "password": "your-password"
  }

 ## Endpoints
| Method        | Endpoint      | Description       |
| ------------- | ------------- | ----------------- |
| GET           | /             | Index             |
| POST          | /auth/login   | login             |
| __Questions__ |
| POST          | /questions    | Add a question    |
| GET           | /questions    | Get all questions |
| GET           | /questions/12 | Get question 12   |
| __Meetups__   |
| POST          | /meetups      | Add a meetup      |
| GET           | /meetups      | Get all meetups   |
| GET           | /meetups/2    | Get meetup 2      |
| PUT           | /meetups/2    | Update meetup 2   |
| DELETE        | /meetups/2    | Delete meetup 2   |
