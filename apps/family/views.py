# from rest_framework import viewsets
#
# from apps.family.models import Family, FamilyGarden, FamilyTree, Branch, PlantedTree
# from apps.family.serializers import FamilySerializer, FamilyGardenSerializer, FamilyTreeSerializer, BranchSerializer, \
#     PlantedTreeSerializer, FamilyRegisterSerializer, FamilyListSerializer, FamilyDetailSerializer, \
#     FamilyTreeDetailSerializer, FamilyTreeListSerializer, FamilyTreeRegisterSerializer, BranchDetailSerializer, \
#     BranchListSerializer, BranchRegisterSerializer, PlantedTreeDetailSerializer, PlantedTreeListSerializer, \
#     PlantedTreeRegisterSerializer, FamilyGardenDetailSerializer, FamilyGardenListSerializer, \
#     FamilyGardenRegisterSerializer
#
#
# class FamilyViewSet(viewsets.ModelViewSet):
#     queryset = Family.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return FamilyRegisterSerializer
#         elif self.action == 'list':
#             return FamilyListSerializer
#         elif self.action in ['retrieve', 'update', 'partial_update']:
#             return FamilyDetailSerializer
#         return FamilySerializer
#
#
# class FamilyGardenViewSet(viewsets.ModelViewSet):
#     queryset = FamilyGarden.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return FamilyGardenRegisterSerializer
#         elif self.action == 'list':
#             return FamilyGardenListSerializer
#         elif self.action in ['retrieve', 'update', 'partial_update']:
#             return FamilyGardenDetailSerializer
#         return FamilyGardenSerializer
#
#
# class FamilyTreeViewSet(viewsets.ModelViewSet):
#     queryset = FamilyTree.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return FamilyTreeRegisterSerializer
#         elif self.action == 'list':
#             return FamilyTreeListSerializer
#         elif self.action in ['retrieve', 'update', 'partial_update']:
#             return FamilyTreeDetailSerializer
#         return FamilyTreeSerializer
#
#
# class BranchViewSet(viewsets.ModelViewSet):
#     queryset = Branch.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return BranchRegisterSerializer
#         elif self.action == 'list':
#             return BranchListSerializer
#         elif self.action in ['retrieve', 'update', 'partial_update']:
#             return BranchDetailSerializer
#         return BranchSerializer
#
#
# class PlantedTreeViewSet(viewsets.ModelViewSet):
#     queryset = PlantedTree.objects.all()
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return PlantedTreeRegisterSerializer
#         elif self.action == 'list':
#             return PlantedTreeListSerializer
#         elif self.action in ['retrieve', 'update', 'partial_update']:
#             return PlantedTreeDetailSerializer
#         return PlantedTreeSerializer
