import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from question.models import Question, Comment
from meetup.models import Meeting



UserModel = get_user_model()


class APIUserAPITestCase(APITestCase):
    """Test suite for the comment API views."""

    @pytest.mark.django_db
    def setUp(self):
        """Define the test client and other test variables."""

        # Create user
        self.user = UserModel.objects.create(
            username='test', email='test@test.com', password='test123')
        # Create superuser
        self.admin = UserModel.objects.create(
            username='admin', email='admin@example.com', password='admin12345',
            is_superuser=True
        )
        # Create meetup
        self.meetup = Meeting.objects.create(
            id=1, title='The Django Meetup', date='2019-03-07', start='10:21:39',
            end='12:21:39', created_by=self.admin, created_at='2019-03-07 12:21:39')
        # Add a new question to a meetup
        self.question = Question.objects.create(
            id=1, title='Question title', body='Question body', created_by=self.user,
            meetup_id=self.meetup)
        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class TestCommentList(APIUserAPITestCase):
    """Test suite for comment list."""

    @pytest.mark.django_db
    def test_can_get_comment_list(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_cannot_get_comment_list_with_invalid_meetup(self):
        url = reverse('comment', kwargs={'meetup_id': 100, 'question_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_cannot_get_comment_list_with_invalid_question(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_can_post_a_comment(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytest.mark.django_db
    def test_can_post_a_comment_with_invalid_meetup(self):
        url = reverse('comment', kwargs={'meetup_id': 100, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_can_post_a_comment_with_invalid_question(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 100})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_can_post_a_comment_with_missing_field(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCommentDetail(APIUserAPITestCase):
    """Test suite for comment detail."""

    @pytest.mark.django_db
    def test_can_get_a_single_comment(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_can_get_a_single_comment_invalid_meetup(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 100, 'question_id': 1, 'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_can_get_a_single_comment_invalid_question(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 100, 'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_cannot_get_a_missing(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 28})
        response = self.client.get(url)
        self.assertEqual(response.json()['error'], 'Comment not found')

    # @pytest.mark.django_db
    # def test_can_update_a_comment(self):
    #     post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
    #     data = {
    #         "comment": "blabla....",
    #         "question": 1
    #     }
    #     self.client.post(post_url, data, format="json")
    #     update_url = reverse('comment_detail',
    #                          kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 2})
    #     update_data = {
    #         "comment": "blabla....ck sheep",
    #         "question": 1
    #     }
    #     self.client.put(update_url, update_data, format="json")
    #     # check comment has been updated
    #     get_url = reverse('comment_detail',
    #                       kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 2})
    #     response = self.client.get(get_url)
    #     # self.assertEqual(response.json()['comment'], 'blabla....ck sheep')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_cannot_update_a_comment_with_invalid_meetup(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        update_url = reverse('comment_detail',
                             kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 2})
        update_data = {
            "comment": "blabla....ck sheep",
            "question": 1
        }
        self.client.put(update_url, update_data, format="json")
        # check comment has been updated
        get_url = reverse('comment_detail',
                          kwargs={'meetup_id': 100, 'question_id': 1, 'pk': 2})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_cannot_update_a_comment_with_invalid_question(self):
        post_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(post_url, data, format="json")
        update_url = reverse('comment_detail',
                             kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 2})
        update_data = {
            "comment": "blabla....ck sheep",
            "question": 1
        }
        self.client.put(update_url, update_data, format="json")
        # check comment has been updated
        get_url = reverse('comment_detail',
                          kwargs={'meetup_id': 1, 'question_id': 100, 'pk': 2})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # @pytest.mark.django_db
    # def test_can_remove_a_single_comment(self):
    #     post_comment_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
    #     data = {
    #         "comment": "bolingoli....",
    #         "question": 1
    #     }
    #     self.client.post(post_comment_url, data, format="json")
    #     url = reverse('comment_detail',
    #                   kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 1})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @pytest.mark.django_db
    def test_can_remove_comment_with_invalid_meetup(self):
        post_comment_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "bolingoli....",
            "question": 1
        }
        self.client.post(post_comment_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 100, 'question_id': 1, 'pk': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_can_remove_comment_with_invalid_question(self):
        post_comment_url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "bolingoli....",
            "question": 1
        }
        self.client.post(post_comment_url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 100, 'pk': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
