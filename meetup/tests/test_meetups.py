""" import json

from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    def setUp(self):
        self.meetup = {
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": 1,
            "created_at": "2019-03-07 12:21:39",
        }

        self.meetup2 = {
            "title": "Meetup2 title2",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": 1,
            "created_at": "2019-03-07 12:21:39",
        }

        self.meetup_wrong = {
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": 1,
            "created_at": "2019-03-07 12:21:39",
        }

    def test_post_meetup(self):
        response = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Meetup title" in str(response.data))

    def test_post_wrong_meetup(self):
        response = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup_wrong),
        )
        self.assertEqual(response.status_code, 400)

    def test_get_meetups(self):
        self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )

        response = self.client.get(reverse("meetings"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Meetup title" in str(response.data))

    def test_put_meetup(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )

        response = self.client.put(
            reverse("meeting", kwargs={"meeting_id": resp.data["id"]}),
            content_type="application/json",
            data=json.dumps(self.meetup2),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Meetup2 title2" in str(response.data))

    def test_put_wrong_meetup(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )

        response = self.client.put(
            reverse("meeting", kwargs={"meeting_id": resp.data["id"]}),
            content_type="application/json",
            data=json.dumps(self.meetup_wrong),
        )

        self.assertEqual(response.status_code, 400)

    def test_get_meetup(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )

        response = self.client.get(
            reverse("meeting", kwargs={"meeting_id": resp.data["id"]})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Meetup title" in str(response.data))

    def test_delete_meetup(self):
        resp = self.client.post(
            reverse("meetings"),
            content_type="application/json",
            data=json.dumps(self.meetup),
        )

        response = self.client.delete(
            reverse("meeting", kwargs={"meeting_id": resp.data["id"]})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deleted' in str(response.data))
 """
