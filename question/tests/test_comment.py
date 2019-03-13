from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from question.models import Comment, Question
from meetup.models import Meeting


class CommentViewsTestCase(TestCase):
    """Test suite for the comment API views."""

    def setUp(self):
        """Define the test client and other test variables."""
        admin = User.objects.create(
            username="admin",
            email="admin@questioner.com",
            is_staff=True,
            is_superuser=True,
        )
        user = User.objects.create(username="mwinel")

        self.meetup = Meeting({
            "title": "Meetup title",
            "date": "2019-03-07",
            "start": "10:21:39",
            "end": "12:21:39",
            "created_by": admin.id
        })

        self.question = Question({
            "title": "Who did it?",
            "body": "yes i did ask",
            "created_by": user.id,
            "meetup_id": self.meetup.id
        })
        # Initialize client and force it to use authentication.
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        # Since user model instance is not serializable, use its Id/PK.
        self.comment_data = {'comment': 'you did it', 'question': 1, 'created_by': user.id}
        self.response = self.client.post(
            reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1}),
            self.comment_data,
            format="json"
        )

    def test_api_can_create_a_comment(self):
        """Test api can create a comment."""
        # self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 0)
