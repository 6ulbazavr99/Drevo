from rest_framework import routers

from .views import FamilyViewSet

router = routers.DefaultRouter()
router.register(r'family', FamilyViewSet)


urlpatterns = []
urlpatterns += router.urls
