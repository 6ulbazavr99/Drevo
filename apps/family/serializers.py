from rest_framework import serializers

from apps.family.models import Family, FamilyMember, FamilyImage


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class FamilyRegisterSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('members', 'parent', 'name',)


class FamilyListSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('id', 'name')


class FamilyDetailSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('name', 'members', 'parent', 'preview', )


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'


class FamilyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyImage
        fields = '__all__'
