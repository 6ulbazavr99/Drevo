from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from apps.plant.models import PlantedTree
from apps.plant.permissions import IsMemberOrAdmin, IsMember, IsPlant
from apps.plant.serializers import PlantedTreeSerializer, PlantedTreeListSerializer, PlantedTreeDetailSerializer
from apps.plant.utils import send_pruning_email, send_watering_email, send_fertilizing_email

User = get_user_model()


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
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsMember()]
        elif self.action == 'my_planted_tree':
            return [IsPlant(), IsMember()]
        return [super(PlantedTreeViewSet, self).get_permissions()]

    @action(detail=False, methods=['get'])
    def my_planted_tree(self, request):
        # planted_tree_watering_email(request.user)
        # check_and_notify_tree_condition(request.user)
        print('action')
        user = request.user
        trees = PlantedTree.objects.filter(user=user)
        for tree in trees:

            check_and_notify_tree_condition(request)
        serializer = PlantedTreeSerializer(trees, many=True)
        return Response(serializer.data)


def check_and_notify_tree_condition(request):
    user = request.user
    tree = user.planted_tree.all().first()
    condition = tree.condition
    print(condition)
    print('check')
    # ('watering', _('Требуется полить')),
    # ('pruning', _('Требуется обрезка')),
    # ('fertilizing', _('Требуется подкормка')),
    # ('good', _('Хорошо')),
    # ('medium', _('Средне')),
    # ('bad', _('Плохо')),
    try:
        if 'watering' in condition:
            send_watering_email(user)
            return JsonResponse({'message': 'Уведомление о поливке отправлено пользователю.'})
        elif 'pruning' in condition:
            send_pruning_email(user)
            return JsonResponse({'message': 'Уведомление об обрезке отправлено пользователю.'})
        elif 'fertilizing' in condition:
            send_fertilizing_email(user)
            return JsonResponse({'message': 'Уведомление о подкормке отправлено пользователю.'})
        else:
            return JsonResponse({'message': 'Дерево в хорошем состоянии, уведомление не требуется.'})

    except User.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден.'}, status=404)
    except PlantedTree.DoesNotExist:
        return JsonResponse({'error': 'Дерево не найдено.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Произошла ошибка: {str(e)}'}, status=500)
