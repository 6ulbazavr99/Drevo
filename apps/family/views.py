from rest_framework import viewsets

from apps.family.models import Family
from apps.family.serializers import FamilySerializer


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
