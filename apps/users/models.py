from django.utils.translation import gettext_lazy as _
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from apps.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(_('Имя пользователя'), max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_('Электронная почта'), unique=True)
    phone = PhoneNumberField(_('Телефон'), blank=True, null=True, unique=True)
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', blank=True, null=True)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    GENDER_CHOICES = [
        ('male', _('Мужской')),
        ('female', _('Женский'))
    ]

    gender = models.CharField(_('Пол'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    patronymic = models.CharField(_('Отчество'), max_length=255, blank=True, null=True)
    birthdate = models.DateField(_('Дата рождения'), blank=True, null=True)
    age = models.IntegerField(_('Возраст'), blank=True, null=True)

    birthplace = models.CharField(_('Место рождения'), max_length=255, blank=True, null=True)
    city = models.CharField(_('Город'), max_length=255, blank=True, null=True)
    country = models.CharField(_('Страна'), max_length=255, blank=True, null=True)

    marriage = models.BooleanField(_('Брак'), default=False, blank=True, null=True)
    partner = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True,
                                related_name='partners', blank=True, verbose_name=_('Партнер'))

    about_me = models.TextField(_('О себе'), blank=True, null=True)
    education = models.CharField(_('Образование'), max_length=255, blank=True, null=True)
    work = models.CharField(_('Работа'), max_length=255, blank=True, null=True)
    alive = models.BooleanField(_('Жив'), default=True, blank=True, null=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} [{self.email}]'

    def save(self, *args, **kwargs):
        if self.birthdate:
            today = datetime.date.today()
            self.age = today.year - self.birthdate.year - (
                    (today.month, today.day) < (self.birthdate.month, self.birthdate.day))

        if not self.username:
            self.username = self.email.split('@')[0] + str(CustomUser.objects.count())
        super().save(*args, **kwargs)
