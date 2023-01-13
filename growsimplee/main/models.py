from django.db import models

# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=200,null=True,blank=True)
    person = models.CharField(max_length=200,null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    locationtype = models.BooleanField()
    productID = models.CharField(max_length=200)

class product(models.Model):
    productID = models.CharField(max_length=200)
    length = models.FloatField(null=True,blank=True)
    breadth = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    volume = models.FloatField(null=True,blank=True)
    delivered = models.BooleanField(default=False)



