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
        if response.status_code == 200:
            response_data = response.json()
            plant_names = [suggestion['plant_name'] for suggestion in response_data.get('suggestions', [])]

            if plant_names:
                plant_name = plant_names[0]
                openai.api_key = openai_api_key
                gpt_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Вы — помощник, обладающий знаниями о растениях."},
                        {"role": "user", "content": f"Расскажите мне о растении {plant_name}."}
                    ]
                )
                description = gpt_response.choices[0].message['content']
                return Response({"plant_name": plant_name, "description": description}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Растение не найдено."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Ошибка при запросе к Plant.id"}, status=response.status_code)
