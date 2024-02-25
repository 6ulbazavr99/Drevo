from rest_framework import serializers

from apps.plant.models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = '__all__'


class PlantedTreeListSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('id', 'user', 'age', 'preview', )


class PlantedTreeDetailSerializer(PlantedTreeSerializer):
    class Meta:
        model = PlantedTree
        fields = ('user', 'condition', 'type', 'age', 'preview', 'address', 'created_at', )
