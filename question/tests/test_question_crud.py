import json
from django.test import TestCase
from django.contrib.auth.models import User
from meetup.models import Meeting

from rest_framework.test import APIClient
import pytest




class TestQuestionViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(
            username="user1",
            email="user1@questioner.com",
            is_superuser=False,
        )
        self.admin = User.objects.create(
            username="admin",
            email="admin@questioner.com",
            is_staff=True,
            is_superuser=True,
        )
        self.meetup = Meeting.objects.create(
            title="Meetup title",
            date="2019-03-07",
            start="10:21:39",
            end="12:21:39",
            created_by=self.admin.id,
            created_at="2019-03-07 12:21:39",
        )
        self.question = {
            "title": "Question 1 title",
            "body": "this is the body of question 1",
        }
        self.question_edited = {
            "title": "Question 1 title - edited",
            "body": "this is the body of question 1",
            "created_by": 1,
        }
        self.question_missing_fields = {
            "body": "this is the body of question 1",
            "created_by": 1,
        }
        self.question_missing_title = {
            "body": "this is the body of question 1",
        }
        self.question_missing_body = {
            "title": "Question 1 title",
        }

    def test_admin_cannot_add_a_question(self):
        self.client.force_authenticate(user=self.admin)

        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Admin is not allowed to add questions')

    def test_anonymous_user_cannot_add_a_question(self):
        # self.client.force_authenticate(user=AnonymousUser)

        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
    #


    def test_user_can_add_a_question_with_missing_data(self):

        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/"
        response1 = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_title),
        )

        response2 = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_body),
        )

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.data['title'][0],"This field is required.")

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.data['body'][0],"This field is required.")

    def test_user_can_add_a_question(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data'][0]['success'], "Question successfully added to meetup")
        self.assertEqual(response.data['data'][0]['question']['meetup_id'], self.meetup.id)
        self.assertEqual(response.data['data'][0]['question']['created_by'], self.user1.id)
        self.assertEqual(response.data['data'][0]['question']['title'], self.question['title'])
        self.assertEqual(response.data['data'][0]['question']['body'], self.question['body'])

    #
    # def test_add_a_question(self):
    #     api_client.force_authenticate(user=admin_user)
    #     resp = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
    #     response = self.client.post(
    #         url,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     self.assertEqual(response.status_code, 201)
    # #
    # def test_error_adding_a_question(self):
    #     resp = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
    #     response = self.client.post(
    #         url,
    #         content_type="application/json",
    #         data=json.dumps(self.question_missing_fields),
    #     )
    #     self.assertEqual(response.status_code, 400)

    # def test_get_questions(self):
    #     resp = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
    #     self.client.post(
    #         url,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_a_question(self):
    #     resp_1 = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
    #     resp_2 = self.client.post(
    #         url_1,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     url_2 = "/meetups/meetings/{}/questions/{}/".format(
    #         resp_1.data["id"], resp_2.data["id"]
    #     )
    #     response = self.client.get(url_2)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_a_question_wrong_id(self):
    #     resp_1 = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url_2 = "/meetups/meetings/{}/questions/{}/".format(
    #         resp_1.data["id"], 234
    #     )
    #     response = self.client.get(url_2)
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_editing_a_question(self):
    #     resp_1 = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
    #     resp_2 = self.client.post(
    #         url_1,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     url_2 = "/meetups/meetings/{}/questions/{}/".format(
    #         resp_1.data["id"], resp_2.data["id"]
    #     )
    #     response = self.client.put(
    #         url_2,
    #         content_type="application/json",
    #         data=json.dumps(self.question_edited),
    #     )
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_editing_a_question_missing_title(self):
    #     resp_1 = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
    #     resp_2 = self.client.post(
    #         url_1,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     url_2 = "/meetups/meetings/{}/questions/{}/".format(
    #         resp_1.data["id"], resp_2.data["id"]
    #     )
    #     response = self.client.put(
    #         url_2,
    #         content_type="application/json",
    #         data=json.dumps(self.question_missing_title),
    #     )
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_deleting_a_question(self):
    #     resp_1 = self.client.post(
    #         reverse("meetings"),
    #         content_type="application/json",
    #         data=json.dumps(self.meetup),
    #     )
    #     url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
    #     resp_2 = self.client.post(
    #         url_1,
    #         content_type="application/json",
    #         data=json.dumps(self.question),
    #     )
    #     url_2 = "/meetups/meetings/{}/questions/{}/".format(
    #         resp_1.data["id"], resp_2.data["id"]
    #     )
    #     response = self.client.delete(url_2, content_type="application/json")
    #     self.assertEqual(response.status_code, 200)
