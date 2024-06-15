from django.db import models


class House(models.Model):
    address = models.CharField(max_length=128)
    coordinates = models.TextField()
    type_object = models.CharField(max_length=128)
    administrative_district = models.CharField(max_length=128)
    municipal_district = models.CharField(max_length=128)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=128)
    unom = models.IntegerField()

    def __str__(self):
        return self.address
