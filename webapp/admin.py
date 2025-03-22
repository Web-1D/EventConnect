from django.contrib import admin
from webapp.models import User, Category, Event, Comment, QAForum

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(QAForum)
