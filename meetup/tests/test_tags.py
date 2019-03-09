from django.urls import reverse
from django.test import TestCase
import json


class TestUrls(TestCase):

    def setUp(self):

        self.tag = {
            "title": "tag_title",
            "created_by": 1
        }

        self.wrong_tag = {
            "created_by": 1
        }

        self.meetuptag = {
            "tag": 1,
            "meeting": 1
        }

        self.wrong_meetuptag = {
            "meeting": 1
        }

        self.meetup = {
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": 1,
            "created_at": "2019-03-07 12:21:39"
        }

        self.client.post(
            reverse('meetings'),
            content_type='application/json',
            data=json.dumps(self.meetup)
        )

    # def tearDown(self):
    #     self.client.delete


    def test_post_tag(self):
        response = self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.tag)
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('tag_title' in str(response.data))

    def test_post_wrong_tag(self):
        response = self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.wrong_tag)
        )
        self.assertEqual(response.status_code, 400)

    def test_get_tags(self):

        self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.tag)
        )

        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tag_title' in str(response.data))

    def test_delete_tag(self):

        resp = self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.tag)
        )

        response = self.client.delete(
            reverse('tag', kwargs={'tag_id': resp.data['id']}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deleted' in str(response.data))

    def test_add_tag_to_meetup(self):

        respt = self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.tag)
        )

        respm = self.client.post(
            reverse('meetings'),
            content_type='application/json',
            data=json.dumps(self.meetup)
        )

        response = self.client.post(
            reverse('meetingtags'),
            content_type='application/json',
            data=json.dumps({'meeting':respm.data['id'], 'tag':respt.data['id']})
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue('meeting' in str(response.data))

    def test_add_wrong_tag_to_meetup(self):
        response = self.client.post(
            reverse('meetingtags'),
            content_type='application/json',
            data=json.dumps(self.wrong_meetuptag)
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_meetuptag(self):

        respt = self.client.post(
            reverse('tags'),
            content_type='application/json',
            data=json.dumps(self.tag)
        )

        respm = self.client.post(
            reverse('meetings'),
            content_type='application/json',
            data=json.dumps(self.meetup)
        )

        resp = self.client.post(
            reverse('meetingtags'),
            content_type='application/json',
            data=json.dumps({'meeting':respm.data['id'], 'tag':respt.data['id']})
        )

        response = self.client.delete(
            reverse('meetingtag', kwargs={'meeting_id': resp.data['meeting'], 'tag_id': resp.data['tag']}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deleted' in str(response.data))
