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
    - export DATABASE_NAME
    - export DATABASE_HOST
    - export DATABASE_USER
    - export DATABASE_PASSWORD


 ## Running the application:
  Open the directory of the application in the terminal and execute:

    python manage.py migrate
    python manage.py runserver

   In a browser type the Url: http//localhost:8000.

 ## Login

  Using postman login with endpoint
   ```
    http://127.0.0.1:8000/auth/login/
  ```
  Provide your credentials under the body tab
  ```
  {
  	"username": "your-username",
	  "password": "your-password"
  }

  ```

 ## Endpoints
| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | /             | Index           |
| POST   | /auth/login   | login           |
| POST   | /questions    | Add a question  |
| GET    | /questions    | Get questions   |
| GET    | /questions/12 | Get question 12 |
