from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.serializers import CustomUserRegisterSerializer, CustomUserListSerializer, CustomUserDetailSerializer, \
    CustomUserSerializer

from apps.users.permissions import IsAccountOwnerOrAdmin, IsAccountOwner


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
