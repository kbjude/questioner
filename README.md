[![Build Status](https://travis-ci.org/kalsmic/questioner.svg?branch=ch-164393776-setup-testing-environment)](https://travis-ci.org/kalsmic/questioner) [![Coverage Status](https://coveralls.io/repos/github/kalsmic/questioner/badge.svg?branch=master)](https://coveralls.io/github/kalsmic/questioner?branch=master)

# Questioner
by The dojos


Questioner is ...


## Installation:
  - Clone this repository.
  - Setup a virtual environment and activate it.
  - Install the requirements.txt
  - Add a ".env" file that has:
    - export DJANGO_SETTINGS_MODULE="questioner.settings"


## Running the application:
  Open the directory of the application in the terminal and execute:

    python manage.py migrate
    python manage.py runserver
    
  Command to run tests.
  
    pytest  
    
  In a browser type the Url: http//localhost:8000.


## Endpoints
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET    | /        | Index       |
