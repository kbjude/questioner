from django.contrib import admin

from .models import Meeting
from .models import Tag
from .models import MeetingTag

admin.site.register(Meeting)
admin.site.register(Tag)
admin.site.register(MeetingTag)
