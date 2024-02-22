from rest_framework import serializers

from apps.family.models import Family


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'
