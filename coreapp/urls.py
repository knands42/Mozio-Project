from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProviderViewSet, ServiceAreaViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet)
router.register(r'service-areas', ServiceAreaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('service-areas/polygons/', ServiceAreaViewSet.as_view({'get': 'list_polygons'})),
]
