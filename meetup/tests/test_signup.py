from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestSignUp(APITestCase):
    def test_signup(self):
        """
        Ensure we can signup a user.
        """
        url = reverse('signup')
        data = {
	            'username': 'bison',
                'email': 'bisonlou@gmail.com',
	            'password': 'Pa$$word123',
               }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)