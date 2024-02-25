from django.contrib import admin

from . import models
from .models import Chat, Message

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(Chat)
admin.site.register(Message)