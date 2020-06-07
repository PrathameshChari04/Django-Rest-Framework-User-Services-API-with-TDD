from django.urls import path, include
from rest_framework.routers import DefaultRouter

from services import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('components', views.ComponentViewSet)
router.register('services', views.ServicesViewSet)

app_name = 'services'

urlpatterns = [
    path('', include(router.urls)),
]


