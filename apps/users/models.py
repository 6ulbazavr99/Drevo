from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


from apps.users.managers import CustomUserManager


class Profile(models.Model):
    mother = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='children_as_mother', blank=True)
    father = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='children_as_father', blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    marriage = models.BooleanField(default=False, blank=True, null=True)
    partner = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='partners', blank=True)
    about_me = models.TextField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    work = models.CharField(max_length=255, blank=True, null=True)
    images = models.ImageField(upload_to='images/', blank=True, null=True)
    alive = models.BooleanField(default=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
