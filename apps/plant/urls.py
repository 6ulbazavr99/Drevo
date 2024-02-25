from rest_framework import routers

from .views import PlantedTreeViewSet

router = routers.DefaultRouter()
router.register(r'planted-tree', PlantedTreeViewSet)


urlpatterns = []
urlpatterns += router.urls
