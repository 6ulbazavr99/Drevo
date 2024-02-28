from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.plant.models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if PlantedTree.objects.filter(user=user).exists():
            raise ValidationError("У вас уже есть зарегистрированное дерево")
        return PlantedTree.objects.create(user=user, **validated_data)


class PlantedTreeListSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('id', 'user', 'age', 'preview', )


class PlantedTreeRegisterSerializer(PlantedTreeSerializer):

    class Meta:
        model = PlantedTree
        fields = ('type', 'age', )


class PlantedTreeDetailSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('user', 'condition', 'needs', 'type', 'age', 'preview', 'address', 'created_at', )
