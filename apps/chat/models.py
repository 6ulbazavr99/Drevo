from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name='chats',
        verbose_name=_('Participants'),
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Chat {self.id}"

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Chat'),
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
    )
    content = models.TextField(
        _('Content'),
    )
    timestamp = models.DateTimeField(
        _('Timestamp'),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Message from {self.sender} in {self.chat}"

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')