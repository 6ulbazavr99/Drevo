from django.urls import path
from rest_framework import routers

from .views import PlantedTreeViewSet, IdentifyPlantView

router = routers.DefaultRouter()
router.register(r'planted-tree', PlantedTreeViewSet)


urlpatterns = [
    path('identify_plant/', IdentifyPlantView.as_view(), name='identify_plant'),
]
urlpatterns += router.urls
