import json

from django.urls import reverse

# class TestUrls(TestCase):
#     def setUp(self):
#         # self.client = APIClient()
#         self.admin = User.objects.create(
#             username="joel",
#             email="joel@questioner.com",
#             is_staff=True,
#             is_superuser=True,
#         )


meetup = {
    "title": "Meetup title",
    "date": "2019-03-07",
    "start": "10:21:39",
    "end": "12:21:39",
}

# self.meetup2 = {
#     "title": "Meetup2 title2",
#     "date": "2019-03-07",
#     "start": "10:21:39",
#     "end": "12:21:39",
#     "created_by": 1,
#     "created_at": "2019-03-07 12:21:39",
# }
#
meetup_wrong = {
    "date": "2019-03-07",
    "start": "10:21:39",
    "end": "12:21:39"
}


def test_non_admin_user_cannot_create_meetup(api_client, db, user1):
    api_client.force_authenticate(user=user1)

    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps({
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
        }),
    )
    assert response.data['status'] == 401
    assert response.data['error'] == "Action restricted to Admins!"


def test_post_meetup(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps({
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
        }),
    )
    assert response.status_code == 201
    assert response.data['data'][0]['success'] == "Meet up created successfully"
    assert response.data['data'][0]['meetup']['title'] == meetup["title"]
    assert response.data['data'][0]['meetup']['start'] == meetup["start"]
    assert response.data['data'][0]['meetup']['created_by'] == admin_user.id


def test_post_wrong_meetup(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps(meetup_wrong),
    )
    assert response.status_code == 400
    assert response.data['error']['title'][0] == 'This field is required.'


def test_get_meetups(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(reverse("meetings"))
    assert response.status_code == 200
    assert len(response.data['data'][0]['meetup']) == 1
    assert response.data['data'][0]['meetup'][0]['id'] == meetup1.id
    assert response.data['data'][0]['meetup'][0]['title'] == meetup1.title


def test_non_amin_cannot_edit_meetup(api_client, db, user1, meetup1):
    api_client.force_authenticate(user=user1)

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup),
    )

    assert response.status_code == 401
    assert response.data['status'] == 401
    assert response.data['error'] == "Action restricted to Admins!"


def test_admin_can_edit_meetup(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup),
    )

    assert response.status_code == 200
    assert response.data['data'][0]['meetup']['title'] == meetup['title']
    assert response.data['data'][0]['meetup']['start'] == meetup['start']
    assert response.data['data'][0]['meetup']['end'] == meetup['end']


def test_edit_meetup_with_missing_data(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup_wrong),
    )
    assert response.status_code == 400
    assert response.data['error']['title'][0] == "This field is required."


def test_get_a_meetup(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )
    assert response.status_code == 200
    assert response.data['data'][0]['meetup']['id'] == meetup1.id
    assert response.data['data'][0]['meetup']['title'] == meetup1.title


def test_non_admin_user_cannot_delete_meetup(api_client, db, user1, meetup1):
    api_client.force_authenticate(user=user1)

    response = api_client.delete(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )
    assert response.data['status'] == 401
    assert response.data['error'] == "Action restricted to Admins!"


def test_admin_user_can_delete_meetup(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )
    assert response.data['status'] == 200
    assert response.data['data'][0]['success'] == "Meet deleted successfully"
