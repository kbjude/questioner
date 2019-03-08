from django.urls import reverse, resolve


class TestUrls:

    def test_meetups_url(self):
        path = reverse('meetings')
        assert resolve(path).view_name == 'meetup.views.MeetingList'
