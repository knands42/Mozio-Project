from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point, Polygon
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from .doc_payloads import service_area_create_payload_example, service_area_update_payload_example, provider_create_payload_example

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_summary="List all providers",
        operation_description="Endpoint to list all providers.",
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, required=False, default=1
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER, required=False, default=10
            ),
        ],
        responses={
            200: ProviderSerializer,
            400: 'Bad Request',
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new provider",
        operation_description="Endpoint to create a new provider. The input should include the provider's name, email, phone number, language, and currency.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'currency': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The currency used by the provider, e.g., USD, EUR.',
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The full name of the provider.',
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='The email address of the provider.',
                ),
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The provider\'s phone number.',
                ),
                'language': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The provider\'s preferred language, e.g., en for English.',
                ),
            },
            required=['currency', 'name', 'email', 'phone_number', 'language'],
            example=provider_create_payload_example
        ),
        responses={
            201: ProviderSerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_summary="List all service areas",
        operation_description="Endpoint to list all service areas.",
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, required=False, default=1
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER, required=False, default=10
            ),
        ],
        responses={
            200: ProviderSerializer,
            400: 'Bad Request',
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'provider': openapi.Schema(type=openapi.TYPE_STRING, description='UUID of the provider'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the service area'),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Price in integer (divide by 10 to show to client)'),
                'area': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_NUMBER)
                    ),
                    description='Coordinates of the polygon defining the service area, the longitude and latitude of each point respectively'
                ),
            },
            example=service_area_create_payload_example
        )
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        
        try:
            # Convert area coordinates to a MultiPolygon
            poligon = Polygon(data['area'])
            
            # Get the provider
            provider = Provider.objects.get(id=data['provider'])
            
            # Create the ServiceArea
            service_area = ServiceArea.objects.create(
                name=data['name'],
                price=data['price'],
                area=poligon,
                provider=provider
            )
            
            serializer = self.get_serializer(service_area)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Provider.DoesNotExist:
            return Response({'error': 'Provider not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'provider': openapi.Schema(type=openapi.TYPE_STRING, description='UUID of the provider'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the service area'),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Price in integer (divide by 10 to show to client)'),
                'area': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_NUMBER)
                    ),
                    description='Coordinates of the polygon defining the service area, the longitude and latitude of each point respectively'
                ),
            },
            example=service_area_update_payload_example
        )
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        
        try:
            # Convert area coordinates to a MultiPolygon
            poligon = Polygon(data['area'])
            
            # Get the provider
            provider = Provider.objects.get(id=data['provider'])
            
            # Update the ServiceArea
            instance.name = data['name']
            instance.price = data['price']
            instance.area = poligon
            instance.provider = provider
            instance.save()
            
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Provider.DoesNotExist:
            return Response({'error': 'Provider not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LocateAreaViewSet(APIView):
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'lat', openapi.IN_QUERY, description="Latitude of the point", type=openapi.TYPE_NUMBER, required=True, default="-25.439479625088097"
            ),
            openapi.Parameter(
                'lng', openapi.IN_QUERY, description="Longitude of the point", type=openapi.TYPE_NUMBER, required=True, default="-49.258157079808775"
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the service area'),
                        'provider_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the provider'),
                        'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Price of the service area')
                    }
                ),
                description='List of service areas that contain the given point'
            ),
            400: 'Bad Request: Invalid lat/lng format or missing parameters'
        },
        operation_summary="List Service Areas by Lat/Lng",
        operation_description="Returns a list of service areas that contain the provided latitude and longitude point. The response includes the name of the service area, the provider name, and the price."
    )
    def get(self, request, *args, **kwargs):
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