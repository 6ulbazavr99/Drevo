from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Chat(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name='chats',
        verbose_name=_('Участники'),
    )
    created_at = models.DateTimeField(
        _('Создано'),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Чат {self.id}"

    class Meta:
        verbose_name = _('Чат')
        verbose_name_plural = _('Чаты')


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Чат'),
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Отправитель'),
    )
    content = models.TextField(
        _('Содержание'),
    )
    timestamp = models.DateTimeField(
        _('Временная метка'),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Сообщение от {self.sender} в {self.chat}"

    class Meta:
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')
