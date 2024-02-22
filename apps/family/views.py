from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.family.models import Family, FamilyImage, FamilyMember
from apps.family.serializers import FamilySerializer, FamilyImageSerializer, FamilyMemberSerializer, \
    FamilyDetailSerializer, FamilyListSerializer, FamilyRegisterSerializer


User = get_user_model()


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FamilyRegisterSerializer
        elif self.action == 'list':
            return FamilyListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return FamilyDetailSerializer
        return FamilySerializer

    def perform_create(self, serializer):
        family = serializer.save()
        print(serializer)
        members = self.request.data.get('members', [])
        print(members)
        for member in members:
            user = User.objects.get(pk=member['user'])
            FamilyMember.objects.create(
                family=family,
                user=user,
                role=member['role']
            )


class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer


class FamilyImageViewSet(viewsets.ModelViewSet):
    queryset = FamilyImage.objects.all()
    serializer_class = FamilyImageSerializer
