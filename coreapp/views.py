from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from django.db import IntegrityError

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
    # TOOD: Fix 409 exception
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
