from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


from apps.users.managers import CustomUserManager

import datetime


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='profile')

    mother = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                               related_name='children_as_mother', blank=True)
    father = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                               related_name='children_as_father', blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    birthplace = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    marriage = models.BooleanField(default=False, blank=True, null=True)
    partner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                related_name='partners', blank=True)

    about_me = models.TextField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    images = models.ImageField(upload_to='images/', blank=True, null=True)
    alive = models.BooleanField(default=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Профиль {self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if self.birthdate:
            today = datetime.date.today()
            self.age = today.year - self.birthdate.year - (
                        (today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        super(Profile, self).save(*args, **kwargs)
