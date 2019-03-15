from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
import json


class TestLogin(APITestCase):
    def test_login_with_wrong_email(self):
        """
        Ensure we cannot signup with wrong email.
        """
        data = {"username": "bison", "password": "12345", "email": "biso.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'], [
            "Enter a valid email address."
        ])

    def test_get_profile(self):
        """
        Ensure we can logout.
        """

        data = User.objects.create(
            username="user1", email="user1@questioner.com", is_superuser=False)
        self.client.force_authenticate(user=data)

        url = "/accounts/profile/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        data = {"username": "bisonlou", "password": "Pa$$word123",
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_signup_duplicate_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        self.superuser = User.objects.create_superuser(
            "user1", "kalulearthur@gmail.com", "Pa$$word123"
        )
        data = {"username": "user1", "password": "Pa$$word123",
                "email": "kalulearthur@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'], [
                         'This field must be unique.'])
        self.assertEqual(response.data['errors']['username'], [
                         'This field must be unique.'])
