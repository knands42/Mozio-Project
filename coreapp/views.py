from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def list_polygons(self, request, *args, **kwargs):
        lat = float(request.query_params.get('lat'))
        lng = float(request.query_params.get('lng'))
        point = Point(lng, lat)
        
        service_areas = ServiceArea.objects.filter(area__contains=point)

        response_data = [{
            'name': area.name,
            'provider_name': area.provider.name,
            'price': area.price
        } for area in service_areas]

        return Response(response_data)
