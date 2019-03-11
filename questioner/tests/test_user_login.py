from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestLogin(APITestCase):
    def test_login(self):
        """
        Ensure we can login a user.
        """
        self.create_user()
        data = {"username": "bison", "password": "Pa$$word123"}
        response = self.login(data)
        self.assertEqual(response.status_code, 200)

    def test_login_without_password(self):
        """
        Ensure we cannot login without a password.
        """
        self.create_user()
        data = {"username": "bison", "password": ""}
        response = self.login(data)
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        """
        Ensure we cannot login with a wrong password.
        """
        self.create_user()
        data = {"username": "bison", "password": "12345"}
        response = self.login(data)
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_username(self):
        """
        Ensure we cannot login with a wrong username.
        """
        self.create_user()
        data = {"username": "bisonlou", "password": "Pa$$word123"}
        response = self.login(data)
        self.assertEqual(response.status_code, 400)

    def create_user(self):
        self.superuser = User.objects.create_superuser(
            "bison", "bisonlou@gmail.com", "Pa$$word123"
        )

    def login(self, kwags):
        self.username = kwags.get("username")
        self.password = kwags.get("password")

        url = reverse("login")
        data = {"username": self.username, "password": self.password}
        return self.client.post(url, data, format="json")
