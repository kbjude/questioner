from django.contrib.auth.models import User
from meetup.models import Meeting
from question.models import Question
from comment.models import Comment
from django.urls import reverse
from rest_framework.test import APITestCase


class TestUserListing(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
                            username='test'
                        )
        self.admin = User.objects.create(
                            username='admin',
                            is_superuser=True
                        )

        self.meetup = Meeting.objects.create(
                            id=1,
                            title='The Django Meetup',
                            date='2019-03-07',
                            start='10:21:39',
                            end='12:21:39',
                            created_by=self.admin,
                            created_at='2019-03-07 12:21:39'
                        )

        self.question = Question.objects.create(
                            id=1,
                            title='Question title',
                            body='Question body',
                            created_by=self.user,
                            meetup_id=self.meetup
                        )

        self.comment = Comment.objects.create(
                            id=1,
                            comment='comment....',
                            question=self.question,
                            created_by=self.user,
                        )

    def test_succesful_comment_answer_toggle(self):
        """
        Ensure admin can toggle a comment to an answer
        """

        url = reverse("toggle_answer",
                      kwargs={'meetup_id': self.meetup.id,
                              'question_id': self.question.id,
                              'pk': self.comment.id
                              }
                      )
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, format="json")

        self.assertEqual(response.status_code, 200)

    def test_non_admin_comment_answer_toggle(self):
        """
        Ensure non admin cannot toggle a comment to an answer
        """

        url = reverse("toggle_answer",
                      kwargs={'meetup_id': self.meetup.id,
                              'question_id': self.question.id,
                              'pk': self.comment.id
                              }
                      )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, format="json")

        self.assertEqual(response.status_code, 403)

    def test_non_existent_meetup(self):
        """
        Ensure non admin cannot toggle a comment to an answer
        """

        url = f"/meetups/{self.meetup.id}/questions/{self.question.id}/comment/100/toggle_answer/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, format="json")

        self.assertEqual(response.status_code, 404)
