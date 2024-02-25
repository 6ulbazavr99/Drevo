from random import randint
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000, blank=True)
    preview = models.ImageField(upload_to='images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.title[:25]}'

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/')

    @staticmethod
    def generate_name():
        return 'image' + str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImage, self).save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



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
