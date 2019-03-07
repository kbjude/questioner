from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestLogin(APITestCase):
    def test_login(self):
        """
        Ensure we can login a user.
        """
        url = reverse('signup')
        data = {
	            'username': 'bison',
                'email': 'bisonlou@gmail.com',
	            'password': 'Pa$$word123',
               }
        self.client.post(url, data, format='json')

        url = reverse('login')
        data = {
	            'username': 'bison',
	            'password': 'Pa$$word123',
               }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)