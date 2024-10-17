from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer
from .doc_payloads import service_area_update_payload_example, provider_create_payload_example, service_area_create_payload_example
from .serializers import ServiceAreaSerializer
from django.contrib.gis.geos import Polygon


class ProviderAPITests(APITestCase):
    
    def setUp(self):
        # Create several providers
        for i in range(10):
            Provider.objects.create(
                name=f'Provider {i}',
                email=f'provider{i}@example.com',
                phone_number=f'99983441{i}',
                language='en',
                currency='USD'
            )
    
    def test_create_provider_success(self):
        """
        Ensure we can create a new provider with valid data.
        """
        url = reverse('provider-list')
        
        response = self.client.post(url, provider_create_payload_example, format='json')

        # Check that the response status is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data matches the input data
        self.assertEqual(response.data['name'], provider_create_payload_example['name'])
        self.assertEqual(response.data['email'], provider_create_payload_example['email'])
        self.assertEqual(response.data['currency'], provider_create_payload_example['currency'])

        # Optionally, you can also check if the provider exists in the database
        provider = Provider.objects.get(email=provider_create_payload_example['email'])
        self.assertIsNotNone(provider)

    def test_create_provider_bad_request(self):
        """
        Ensure we get a 400 Bad Request for missing required fields.
        """
        url = reverse('provider-list')
        data = {
            'currency': 'USD',
            # 'name': 'John Doe',  # Name is missing, which should cause a 400 error
            'email': 'johndoe@example.com',
            'phone_number': '999834414',
            'language': 'en'
        }
        
        response = self.client.post(url, data, format='json')

        # Check that the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response message contains the missing field error
        self.assertIn('name', response.data)

    def test_list_providers(self):
        """
        Ensure we can list all providers.
        """
        url = reverse('provider-list')
        response_page_1 = self.client.get(url, {'page': 1, 'page_size': 5}, format='json')
        self.assertEqual(response_page_1.status_code, status.HTTP_200_OK)

        # Check that the total count of providers is 10
        self.assertEqual(response_page_1.data['count'], 10)

        # Verify the data for the first provider in the response
        first_provider = response_page_1.data['results'][0]
        self.assertEqual(first_provider['name'], 'Provider 0')
        
        response_page_2 = self.client.get(url, {'page': 2, 'page_size': 5}, format='json')
        self.assertEqual(response_page_2.status_code, status.HTTP_200_OK)
        
        # Verify the data for the first provider in the response
        first_provider = response_page_2.data['results'][0]
        self.assertEqual(first_provider['name'], 'Provider 5')
        

    def test_retrieve_provider(self):
        """
        Ensure we can retrieve a specific provider.
        """
        provider = Provider.objects.first()
        url = reverse('provider-detail', args=[provider.id])
        response = self.client.get(url, format='json')

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the provider data
        serializer = ProviderSerializer(provider)
        self.assertEqual(response.data, serializer.data)
        
    def test_update_provider(self):
        """
        Ensure we can update a provider.
        """
        provider = Provider.objects.first()
        url = reverse('provider-detail', args=[provider.id])
        data = {
            'name': 'John Doe 2',
            'email': 'johndoe2@email.com',
            'phone_number': '1234567890',
            'language': 'German',
            'currency': 'EUR'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the provider data has been updated
        provider.refresh_from_db()
        self.assertEqual(provider.name, data['name'])
        self.assertEqual(provider.email, data['email'])
        self.assertEqual(provider.phone_number, data['phone_number'])
        self.assertEqual(provider.language, data['language'])
        self.assertEqual(provider.currency, data['currency'])
    
    def test_delete_provider(self):
        """
        Ensure we can delete a provider.
        """
        provider = Provider.objects.first()
        url = reverse('provider-detail', args=[provider.id])
        response = self.client.delete(url, format='json')
        
        # Check that the response status is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the provider has been deleted
        with self.assertRaises(Provider.DoesNotExist):
            provider.refresh_from_db()
        
class ServiceAPITests(APITestCase):
    
    def setUp(self):
       # Create a provider
        provider = Provider.objects.create(
            name=f'Provider',
            email=f'provider@example.com',
            phone_number=f'999834410',
            language='en',
            currency='USD'
        )
    
        # Create several services for the provider
        for i in range(10):
            ServiceArea.objects.create(
                provider=provider,
                name=f'Service {i}',
                price=i*10,
                area='POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'
            )
            
    def test_create_service_success(self):
        """
        Ensure we can create a new service with valid data.
        """
        provider = Provider.objects.first()
        url = reverse('service_area-list')
        service_area_create_payload_example.update({'provider': provider.id})
        
        response = self.client.post(url, service_area_create_payload_example, format='json')

        # Check that the response status is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data matches the input data
        self.assertEqual(response.data['name'], service_area_create_payload_example['name'])
        self.assertEqual(response.data['price'], service_area_create_payload_example['price'])
    
        # Check if the service was created in the database
        service = ServiceArea.objects.get(name=service_area_create_payload_example['name'])
        self.assertIsNotNone(service)
    
    def test_list_services(self):
        """
        Ensure we can list all services.
        """
        url = reverse('service_area-list')
        response_page_1 = self.client.get(url, {'page': 1, 'page_size': 5}, format='json')
        self.assertEqual(response_page_1.status_code, status.HTTP_200_OK)

        # Check that the total count of services is 10
        self.assertEqual(response_page_1.data['count'], 10)

        # Verify the data for the first service in the response
        first_service = response_page_1.data['results'][0]
        self.assertEqual(first_service['name'], 'Service 0')
        
        response_page_2 = self.client.get(url, {'page': 2, 'page_size': 5}, format='json')
        self.assertEqual(response_page_2.status_code, status.HTTP_200_OK)
        
        # Verify the data for the first service in the response
        first_service = response_page_2.data['results'][0]
        self.assertEqual(first_service['name'], 'Service 5')
        
    def test_retrieve_service(self):
        """
        Ensure we can retrieve a specific service.
        """
        service = ServiceArea.objects.first()
        url = reverse('service_area-detail', args=[service.id])
        response = self.client.get(url, format='json')

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the service data
        serializer = ServiceAreaSerializer(service)
        self.assertEqual(response.data, serializer.data)
        
    def test_update_service(self):
        """
        Ensure we can update a service.
        """
        service = ServiceArea.objects.first()
        url = reverse('service_area-detail', args=[service.id])
        service_area_update_payload_example.update({'provider': service.provider.id})
        response = self.client.put(url, service_area_update_payload_example, format='json')
        
        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the service data has been updated
        service.refresh_from_db()
        self.assertEqual(service.name, service_area_update_payload_example['name'])
        self.assertEqual(service.price, service_area_update_payload_example['price'])
        
    def test_delete_service(self):
        """
        Ensure we can delete a service.
        """
        service = ServiceArea.objects.first()
        url = reverse('service_area-detail', args=[service.id])
        response = self.client.delete(url, format='json')
        
        # Check that the response status is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the service has been deleted
        with self.assertRaises(ServiceArea.DoesNotExist):
            service.refresh_from_db()
            
class LocateAreaTests(APITestCase):
    
    def setUp(self):
       # Create a provider
        provider = Provider.objects.create(
            name=provider_create_payload_example.get('name'),
            email=provider_create_payload_example.get('email'),
            phone_number=provider_create_payload_example.get('phone_number'),
            language=provider_create_payload_example.get('language'),
            currency=provider_create_payload_example.get('currency')
        )
    
        # Create several services for the provider
        ServiceArea.objects.create(
            provider=provider,
            name=service_area_create_payload_example.get('name'),
            price=service_area_create_payload_example.get('price'),
            area=Polygon(service_area_create_payload_example.get('area'))
        )
            
    def test_locate_area_success(self):
        """
        Ensure we can locate a service area given a point.
        """
        url = reverse('locate_service_areas')
        data = {
            'lat': "-25.439479625088097",
            'lng': "-49.258157079808775"
        }
        
        response = self.client.get(url, query_params=data, format='json')
        
        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response data matches the expected service area
        self.assertEqual(response.data[0]['name'], service_area_create_payload_example.get('name')) # Curitiba
        self.assertEqual(response.data[0]['price'], service_area_create_payload_example.get('price')) # 10000