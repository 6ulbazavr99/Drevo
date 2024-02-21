from rest_framework import serializers

from apps.family.models import Family, FamilyTree, Branch, PlantedTree, FamilyGarden


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class FamilyRegisterSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('parents', 'children', 'description', )


class FamilyDetailSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('family_name', 'parents', 'children', 'description', 'images', 'tree', )


class FamilyListSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('id', 'family_name', )


class FamilyTreeSerializer(serializers.ModelSerializer):
    family_name = serializers.SerializerMethodField()

    class Meta:
        model = FamilyTree
        fields = '__all__'

    def get_family_name(self, obj):
        try:
            family = Family.objects.get(tree=obj)
            return family.family_name
        except Family.DoesNotExist:
            return f'Семейное древо №{obj.pk}'
        except Exception as e:
            return f'Ошибка: {str(e)}'


class FamilyTreeRegisterSerializer(FamilyTreeSerializer):
    family_name = None

    class Meta:
        model = FamilyTree
        exclude = ('id', 'created_at', 'updated_at', 'images', )


class FamilyTreeListSerializer(FamilyTreeSerializer):
    class Meta:
        model = FamilyTree
        fields = ('id', 'family_name', )


class FamilyTreeDetailSerializer(FamilyTreeSerializer):
    class Meta:
        model = FamilyTree
        exclude = ('id', 'created_at', 'updated_at', )


class BranchSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user')

    class Meta:
        model = Branch
        fields = '__all__'


class BranchListSerializer(BranchSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'user_name', )


class BranchDetailSerializer(BranchSerializer):
    class Meta:
        model = Branch
        fields = ('user_name', 'role', 'user', )


class BranchRegisterSerializer(BranchSerializer):
    class Meta:
        model = Branch
        fields = ('user', 'role', )


class PlantedTreeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='branch.user')

    class Meta:
        model = PlantedTree
        fields = '__all__'


class PlantedTreeRegisterSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('branch', )


class PlantedTreeListSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('id', 'user', )


class PlantedTreeDetailSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('user', 'branch', 'images', )


class FamilyGardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyGarden
        fields = '__all__'


class FamilyGardenListSerializer(FamilyGardenSerializer):
    class Meta:
        model = FamilyGarden
        fields = ('id', 'family_name', )


class FamilyGardenRegisterSerializer(FamilyGardenSerializer):
    class Meta:
        model = FamilyGarden
        fields = ('family_name', 'description', )


class FamilyGardenDetailSerializer(FamilyGardenSerializer):
    class Meta:
        model = FamilyGarden
        exclude = ('id', 'updated_at', )
