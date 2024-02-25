from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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

    @action(['GET'], detail=False)
    def profile(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_online(self, request, pk=None):
        user = self.get_object()
        user.is_online = True
        user.save()
        return Response({'status': 'Пользователь сейчас в сети'})

    @action(detail=True, methods=['post'])
    def set_offline(self, request, pk=None):
        user = self.get_object()
        user.is_online = False
        user.save()
        return Response({'status': 'Пользователь сейчас не в сети'})
