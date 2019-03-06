# Questioner
by The dojos

#### Application test badges
##### [![Build Status](https://travis-ci.org/AtamaZack/questioner.svg?branch=develop)](https://travis-ci.org/AtamaZack/questioner)

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
    
  In a browser type the Url: http//localhost:8000.


## Endpoints
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET    | /        | Index       |
