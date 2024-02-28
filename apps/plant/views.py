from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.plant.models import PlantedTree
from apps.plant.permissions import IsTreePlanted, IsFamilyMember, IsOwnerOrAdmin, IsOwner
from apps.plant.serializers import PlantedTreeSerializer, PlantedTreeListSerializer, PlantedTreeDetailSerializer, \
    PlantedTreeRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import base64
import json
import openai
from decouple import config


User = get_user_model()


class PlantedTreeViewSet(viewsets.ModelViewSet):
    queryset = PlantedTree.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantedTreeListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return PlantedTreeDetailSerializer
        elif self.action == 'create':
            return PlantedTreeRegisterSerializer
        return PlantedTreeSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsTreePlanted(), IsOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsTreePlanted(), IsOwner()]
        elif self.action == 'create':
            return [IsFamilyMember()]
        elif self.action == 'my_planted_tree':
            return [IsTreePlanted()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def my_planted_tree(self, request):
        user = request.user
        tree = PlantedTree.objects.get(user=user)
        serializer = PlantedTreeSerializer(tree)
        return Response(serializer.data)


class IdentifyPlantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        plant_id_api_key = config('PLANTID')
        openai_api_key = config('OPENAI')
        plant_id_url = "https://api.plant.id/v2/identify"

        image_data = request.FILES.get('image')
        if not image_data:
            return Response({"error": "Требуется файл изображения."}, status=status.HTTP_400_BAD_REQUEST)

        encoded_image = base64.b64encode(image_data.read()).decode('utf-8')
        headers = {"Content-Type": "application/json"}
        data = {
            "images": [encoded_image],
            "organs": ["leaf"],
            "api_key": plant_id_api_key
        }

        response = requests.post(plant_id_url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            return Response({"error": "Ошибка при запросе к базе данных"}, status=response.status_code)

        response_data = response.json()

        ban_list = ['ficus', 'fungi', 'фикус', 'грибы', 'mushroom', 'insect', 'насекомое', 'dracaena',
                    'mammillaria', 'elongata', 'cymbopogon']

        ban_list = [x.lower() for x in ban_list]
        plant_names = [suggestion['plant_name'] for suggestion in response_data.get('suggestions', [])
                       if all(banned not in suggestion['plant_name'].lower() for banned in ban_list)]

        if not plant_names:
            return Response({"error": "В переданной фотографии не удалось определить дерево"},
                            status=status.HTTP_404_NOT_FOUND)

        plant_name = plant_names[0]
        openai.api_key = openai_api_key
        description_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Опиши подробно растение, учитывая его "
                                              "особенности и возможное использование."},
                {"role": "user", "content": f"Что такое {plant_name}?"}
            ]
        )

        description = description_response.choices[0].message['content'].strip()

        if any(banned in description.lower() for banned in ban_list):
            return Response({"error": "В переданной фотографии не удалось определить дерево"},
                            status=status.HTTP_400_BAD_REQUEST)

        tree_check_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Определи, является ли следующее описание характеристикой дерева."},
                {"role": "user", "content": f"Вот описание: {description}. Является ли это описание деревом?"}
            ]
        )

        tree_check = tree_check_response.choices[0].message['content'].strip()

        is_tree = "да" in tree_check.lower()

        if not is_tree:
            return Response({"error": "В переданной фотографии не удалось определить дерево"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"plant_name": plant_name, "description": description, "is_tree": is_tree},
                        status=status.HTTP_200_OK)
