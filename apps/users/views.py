from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.models import Profile
from apps.users.permissions import IsAccountOwnerOrAdmin, IsAccountOwner, IsProfileOwnerOrAdmin, IsProfileOwner
from apps.users.serializers import CustomUserRegisterSerializer, CustomUserSerializer, CustomUserListSerializer, \
    CustomUserDetailSerializer, ProfileListSerializer, ProfileDetailSerializer, ProfileRegisterSerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserRegisterSerializer
        elif self.action == 'list':
            return CustomUserListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return CustomUserDetailSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAccountOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAccountOwner()]
        elif self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializer
        elif self.action == 'create':
            return ProfileRegisterSerializer
        return ProfileDetailSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsProfileOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsProfileOwner()]
        elif self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
