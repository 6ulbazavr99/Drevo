from rest_framework import routers

from .views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'account', CustomUserViewSet)


urlpatterns = []

urlpatterns += router.urls
