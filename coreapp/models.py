from django.contrib.gis.db import models
import uuid

class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)

    class Meta:
        db_table = 'providers'
        indexes = [
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_provider_name')
        ]
    
    def __str__(self):
        return self.name

class ServiceArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='service_areas')
    name = models.CharField(max_length=255)
    price = models.BigIntegerField() # big integer to avoid operation with decimal values (Just divide by 10 when showing to the client)
    area = models.MultiPolygonField(geography=True)

    class Meta:
        db_table = 'service_areas'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['area']),
        ]


    def __str__(self):
        return self.name
