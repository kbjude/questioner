import json

from django.test import TestCase
from django.urls import reverse


class TestQuestionViews(TestCase):
    def setUp(self):
        self.meetup = {
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": 1,
            "created_at": "2019-03-07 12:21:39",
        }
        self.question = {
            "title": "Question 1 title",
            "body": "this is the body of question 1",
            "created_by": 1,
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
            "created_by": 1,
        }
        self.question_missing_body = {
            "title": "Question 1 title",
            "created_by": 1,
        }

    def test_add_a_question(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 201)

    def test_error_adding_a_question(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_fields),
        )
        self.assertEqual(response.status_code, 400)

    def test_get_questions(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url = "/meetups/meetings/{}/questions/".format(resp.data["id"])
        self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_a_question(self):
        resp_1 = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
        resp_2 = self.client.post(
            url_1,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        url_2 = "/meetups/meetings/{}/questions/{}/".format(
            resp_1.data["id"], resp_2.data["id"]
        )
        response = self.client.get(url_2)
        self.assertEqual(response.status_code, 200)

    def test_get_a_question_wrong_id(self):
        resp_1 = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url_2 = "/meetups/meetings/{}/questions/{}/".format(
            resp_1.data["id"], 234
        )
        response = self.client.get(url_2)
        self.assertEqual(response.status_code, 404)

    def test_editing_a_question(self):
        resp_1 = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
        resp_2 = self.client.post(
            url_1,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        url_2 = "/meetups/meetings/{}/questions/{}/".format(
            resp_1.data["id"], resp_2.data["id"]
        )
        response = self.client.put(
            url_2,
            content_type="application/json",
            data=json.dumps(self.question_edited),
        )
        self.assertEqual(response.status_code, 200)

    def test_editing_a_question_missing_title(self):
        resp_1 = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
        resp_2 = self.client.post(
            url_1,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        url_2 = "/meetups/meetings/{}/questions/{}/".format(
            resp_1.data["id"], resp_2.data["id"]
        )
        response = self.client.put(
            url_2,
            content_type="application/json",
            data=json.dumps(self.question_missing_title),
        )
        self.assertEqual(response.status_code, 400)

    def test_deleting_a_question(self):
        resp_1 = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        url_1 = "/meetups/meetings/{}/questions/".format(resp_1.data["id"])
        resp_2 = self.client.post(
            url_1,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        url_2 = "/meetups/meetings/{}/questions/{}/".format(
            resp_1.data["id"], resp_2.data["id"]
        )
        response = self.client.delete(url_2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
