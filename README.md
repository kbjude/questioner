# Questioner by The dojos

Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log.

## Installation

- Clone this repository.
- Setup a virtual environment and activate it.
- Install the requirements.txt
- Add a ".env" file that has:
- export DJANGO_SETTINGS_MODULE="questioner.settings"

## Running the application

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

