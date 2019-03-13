import json

from django.urls import reverse

""" from django.urls import reverse
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

"""
tag1_data = {
    "title": "tag_title",
}


def test_non_admin_user_cannot_create_tags(api_client, db, user1):
    api_client.force_authenticate(user=user1)

    response = api_client.post(
        reverse("tags"),
        content_type="application/json",
        data=json.dumps(tag1_data),
    )
    assert response.data['status'] == 401
    assert response.data['error'] == "Action restricted to Admins!"


def test_admin_user_cannot_create_tag_with_missing_title(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("tags"),
        content_type="application/json",
        data=json.dumps({}),
    )
    assert response.status_code == 400
    assert response.data['error']['title'][0] == "This field is required."


def test_admin_user_can_create_tags(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("tags"),
        content_type="application/json",
        data=json.dumps(tag1_data),
    )
    assert response.status_code == 201
    assert response.data['data'][0]['success'] == "Tag created successfully"
    assert response.data['data'][0]['tag']['title'] == tag1_data["title"]
    assert response.data['data'][0]['tag']['created_by'] == admin_user.id


def test_get_tags(api_client, db, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(reverse('tags'))

    assert response.status_code == 200
    assert len(response.data['data'][0]['tags']) == 3
    assert isinstance(response.data['data'][0]['tags'], list)


def test_cannot_add_disabled_tag_to_meetup(api_client, db, meetup1, admin_user, disabled_tag):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse('meetingtags', kwargs={"meeting_id": meetup1.id}),

        content_type='application/json',
        data=json.dumps({'meeting': meetup1.id, 'tag': disabled_tag.id})
    )

    assert response.status_code == 403
    assert response.data['status'] == 403
    assert response.data['error'] == "This Tag is disabled."


def test_cannot_add_invalid_tag_to_meetup(api_client, db, meetup1, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse('meetingtags', kwargs={"meeting_id": meetup1.id}),

        content_type='application/json',
        data=json.dumps({'meeting': meetup1.id, 'tag': 75})
    )

    assert response.status_code == 404
    assert response.data == {

        "status": 404,
        "error": "Tag with specified id does not exist.",
    }


def test_add_tag_to_meetup(api_client, db, meetup1, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse('meetingtags', kwargs={"meeting_id": meetup1.id}),

        content_type='application/json',
        data=json.dumps({'meeting': meetup1.id, 'tag': tag_objs[0].id})
    )

    assert response.status_code == 201
    assert response.data['data'][0]['success'] == "Tag successfully added to meetup"
    assert response.data['data'][0]['tag']['meetup'] == meetup1.id
    assert response.data['data'][0]['tag']['created_by'] == admin_user.id


def test_delete_tag(api_client, db, meetup1, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(
        reverse('tag', kwargs={'tag_id': tag_objs[0].id}))

    assert response.status_code == 200
    assert response.data['data'][0]['success'] == "Tag permantely deleted successfully"


def test_soft_a_delete_tag_attached_to_a_meetup(api_client, db, meetup1, admin_user, a_tag, meetup_tag):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(
        reverse('tag', kwargs={'tag_id': a_tag.id}))

    assert response.status_code == 200
    assert response.data['data'][0]['success'] == "Tag soft deleted successfully"
