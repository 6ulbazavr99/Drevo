from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.users.models import Profile
from apps.users.serializers import CustomUserRegisterSerializer, CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserRegisterSerializer
        return CustomUserSerializer


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer