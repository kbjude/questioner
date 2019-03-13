from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestLogin(APITestCase):
    def test_login_with_wrong_email(self):
        """
        Ensure we cannot signup with wrong email.
        """
        data = {
                'username': 'bison',
                'email': 'biso.com',
                'password': 'Pa$$word123',
            }
        response = self.signup(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'], [
            "Enter a valid email address."
        ])

    def test_signup_user_with_invalid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        data = {
                'username': 'bison',
                'email': 'bisonlou@gmail.com'
            }
        response = self.signup(data)
        self.assertEqual(response.status_code, 400)

    def test_signup_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        data = {
                'username': 'bison',
                'email': 'bisonlou@gmail.com',
                'password': 'Pa$$word123',
            }
        response = self.signup(data)
        self.assertEqual(response.status_code, 201)

    def test_signup_duplicate_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        data = {
                'username': 'bison',
                'email': 'bisonlou@gmail.com',
                'password': 'Pa$$word123',
            }
        self.signup(data)
        response = self.signup(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'],
                         ['This field must be unique.'])
        self.assertEqual(response.data['errors']['username'],
                         ['This field must be unique.'])

    def signup(self, data):
        url = reverse('signup')
        return self.client.post(url, data, format='json')
