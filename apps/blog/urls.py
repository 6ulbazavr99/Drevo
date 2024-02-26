from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.blog import views

router = SimpleRouter()
router.register('', views.PostViewSet)


urlpatterns = ([

])
urlpatterns += router.urls
