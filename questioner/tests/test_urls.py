from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):

    def test_welcome_url(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['The Dojos'], "Welcome to Questioner.")
