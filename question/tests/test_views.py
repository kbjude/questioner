from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from question.models import Question, Comment


class TestQuestionModel(TestCase):
    """Test suite for the question model."""

    def setUp(self):
        """Define test client and other test variables."""
        user = User.objects.create(username="lulux")
        self.question_data = 'who killed JFK?'
        self.question = Question(title=self.question_data, created_by=user)

    def test_question_model_returns_a_string_representation(self):
        """Test api returns a readable representation of the question model."""
        self.assertEqual(str(self.question), self.question_data)

class TestQuestionViews(TestCase):
    """Test suite for the question API views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="lulux")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.question_data = {
            'title': 'who killed HBO?',
            'body': 'maybe that boy zero',
            'created_by': user.id}
        self.response = self.client.post(
            reverse('question_view'),
            self.question_data,
            format="json"
        )

    def test_api_can_create_a_question(self):
        """Test api can create a question."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_question(self):
        """Test api can get a question."""
        question = Question.objects.get(id=1)
        response = self.client.get(
            reverse('question_details', kwargs={'pk': question.id}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, question)

class CommentViewsTestCase(TestCase):
    """Test suite for the comment API views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.comment_data = "what kind of question is that?"
        self.comment = Comment(comment=self.comment_data)

    def test_comment_model_returns_a_string_representation(self):
        """Test api returns a readable instance of the comment model."""
        self.assertEqual(str(self.comment), self.comment_data)

    # def test_api_can_create_a_comment(self):
    #     """Test api can create a comment."""
    #     url = reverse('comment-list', kwargs={'question_id': 2})
    #     data = {"comment": "what kind of question is this?"}
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
