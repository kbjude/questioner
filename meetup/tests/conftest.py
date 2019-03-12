import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from meetup.models import Meeting, Tag


@pytest.mark.django_db
@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.fixture
def admin_user():
    return get_user_model().objects.create(
        username="questioner",
        email="admin@questioner.com",
        is_staff=True,
        is_superuser=True
    )


@pytest.mark.django_db
@pytest.fixture
def user1():
    return get_user_model().objects.create(
        username="user1",
        email="user1@questioner.com",
        is_superuser=False
    )


@pytest.mark.django_db
@pytest.fixture
def meetup1(admin_user):
    return Meeting.objects.create(
        title="The Django Meetup",
        date="2019-03-07",
        start="10:21:39",
        end="12:21:39",
        created_by=admin_user,
        created_at="2019-03-07 12:21:39"
    )


@pytest.mark.django_db
@pytest.fixture
def tag_objs(admin_user):
    tags = []
    for tag in ['sports', 'Django', 'API']:
        tags.append(Tag.objects.create(
            title=tag,
            created_by=admin_user
        ))
    return tags


@pytest.mark.django_db
@pytest.fixture
def disabled_tag(admin_user):
    return Tag.objects.create(
        title="Javascript",
        created_by=admin_user,
        active=False
    )
