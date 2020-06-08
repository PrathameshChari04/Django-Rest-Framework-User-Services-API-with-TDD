from django.urls import path, include
from rest_framework.routers import DefaultRouter

from service import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('components', views.ComponentViewSet)
router.register('services', views.ServicesViewSet)

app_name = 'service'

urlpatterns = [
    path('', include(router.urls)),
]


