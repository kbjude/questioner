import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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
        is_superuser=True,
    )

@pytest.mark.django_db
@pytest.fixture
def user1():
    return get_user_model().objects.create(
        username="user1", email="user1@questioner.com", is_superuser=False
    )


# @pytest.mark.django_db
# @pytest.fixture
# def user2():
#     return get_user_model().objects.create(
#         username="user2", email="user2@questioner.com", is_superuser=False
#     )


@pytest.mark.django_db
@pytest.fixture
def staff1():
    return get_user_model().objects.create(
        username="staff1", email="staff1@questioner.com", is_staff = True
    )

@pytest.mark.django_db
@pytest.fixture
def staff2():
    return get_user_model().objects.create(
        username="staff2", email="staff2@questioner.com", is_staff = True,is_superuser=False
    )
