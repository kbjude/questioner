from django.contrib import admin

from .models import Question, Comment,Vote

admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Vote)



# Register your models here.
