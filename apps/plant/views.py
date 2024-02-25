from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.plant.models import PlantedTree
from apps.plant.permissions import IsMemberOrAdmin, IsMember, IsPlant
from apps.plant.serializers import PlantedTreeSerializer, PlantedTreeListSerializer, PlantedTreeDetailSerializer


class PlantedTreeViewSet(viewsets.ModelViewSet):
    queryset = PlantedTree.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantedTreeListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return PlantedTreeDetailSerializer
        return PlantedTreeSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsMemberOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsMember()]
        elif self.action == 'my_planted_tree':
            return [IsPlant(), IsMember()]
        return [super(PlantedTreeViewSet, self).get_permissions()]

    @action(detail=False, methods=['get'])
    def my_planted_tree(self, request):
        user = request.user
        trees = PlantedTree.objects.filter(user=user)
        serializer = PlantedTreeSerializer(trees, many=True)
        return Response(serializer.data)
