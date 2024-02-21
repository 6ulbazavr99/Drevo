from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'', CustomUserViewSet)


urlpatterns = []


urlpatterns += router.urls
