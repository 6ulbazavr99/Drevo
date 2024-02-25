from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from apps.family.models import Family, FamilyImage, FamilyMember
from apps.family.permissions import IsFamilyMember, IsFamilyParentMember
from apps.family.serializers import FamilySerializer, FamilyImageSerializer, FamilyMemberSerializer, \
    FamilyDetailSerializer, FamilyListSerializer, FamilyRegisterSerializer, RecursiveFamilySerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from apps.plant.serializers import PlantedTreeSerializer


User = get_user_model()


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FamilyRegisterSerializer
        elif self.action == 'list':
            return FamilyListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return FamilyDetailSerializer
        return FamilySerializer

    def get_permissions(self):
        if self.action in ('my_tree', 'family_tree', 'father_tree', 'mother_tree', 'family_planted_trees'):
            return [IsFamilyMember()]
        elif self.action in ('destroy', 'update', 'partial_update'):
            return [IsFamilyParentMember()]
        return super(FamilyViewSet, self).get_permissions()

    def perform_create(self, serializer):
        family = serializer.save()
        members = self.request.data.get('members', [])
        for member in members:
            user = User.objects.get(pk=member['user'])
            FamilyMember.objects.create(
                family=family,
                user=user,
                role=member['role']
            )

    @action(detail=True, methods=['get'])
    def family_planted_trees(self, request, pk=None):
        family = self.get_object()
        members = family.members.all()
        trees = []
        for member in members:
            tree = member.planted_tree
            serialized_tree = PlantedTreeSerializer(tree).data
            trees.append({member.first_name: serialized_tree})
        return Response(trees)

    @action(detail=False, methods=['get'])
    def my_tree(self, request):
        user = request.user
        trees = []
        for family_member in FamilyMember.objects.filter(user=user):
            family = family_member.family
            serialized_family = RecursiveFamilySerializer(family).data
            trees.append({user.first_name: serialized_family})
        return Response(trees)

    @action(detail=True, methods=['get'])
    def family_tree(self, request, pk=None):
        family = self.get_object()
        serializer = RecursiveFamilySerializer(family)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def father_tree(self, request, pk=None):
        family = self.get_object()
        father_members = family.members.filter(familymember__role='father')
        father_trees = []
        for father in father_members:
            father_families = father.families.all()
            for father_family in father_families:
                serialized_family = RecursiveFamilySerializer(father_family).data
                father_trees.append({father.first_name: serialized_family})
        return Response(father_trees)

    @action(detail=True, methods=['get'])
    def mother_tree(self, request, pk=None):
        family = self.get_object()
        mother_members = family.members.filter(familymember__role='mother')
        mother_trees = []
        for mother in mother_members:
            mother_families = mother.families.all()
            for mother_family in mother_families:
                serialized_family = RecursiveFamilySerializer(mother_family).data
                mother_trees.append({mother.first_name: serialized_family})
        return Response(mother_trees)


class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer


class FamilyImageViewSet(viewsets.ModelViewSet):
    queryset = FamilyImage.objects.all()
    serializer_class = FamilyImageSerializer
