from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.users.models import Profile
from apps.users.serializers import CustomUserRegisterSerializer, CustomUserSerializer, CustomUserListSerializer, \
    CustomUserDetailSerializer, ProfileListSerializer, ProfileSerializer


User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserRegisterSerializer
        if self.action == 'list':
            return CustomUserListSerializer
        if self.action in ['retrieve', 'update', 'partial_update']:
            return CustomUserDetailSerializer
        return CustomUserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializer
        return ProfileSerializer
