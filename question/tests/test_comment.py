from django.test import TestCase
from question.models import Comment


class CommentViewsTestCase(TestCase):
    """Test suite for the comment API views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.comment_data = "what kind of question is that?"
        self.comment = Comment(comment=self.comment_data)

    def test_comment_model_returns_a_string_representation(self):
        """Test api returns a readable instance of the comment model."""
        self.assertEqual(str(self.comment), self.comment_data)
