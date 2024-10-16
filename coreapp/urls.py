from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProviderViewSet, ServiceAreaViewSet, LocateAreaViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet)
router.register(r'service-areas', ServiceAreaViewSet)
# router.register(r'service-areas/polygons', LocateAreaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('service-areas/polygons', LocateAreaViewSet.as_view(), name='locate-service-areas'),
]
