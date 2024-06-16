from django.db import models


class House(models.Model):
    address = models.CharField(max_length=128)
    coordinates = models.TextField()
    type_object = models.CharField(max_length=128)
    administrative_district = models.CharField(max_length=128)
    municipal_district = models.CharField(max_length=128)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=128)
    unom = models.IntegerField(unique=True)
    unom_houses = models.TextField()

    def __str__(self):
        return self.address


class DataModel(models.Model):
    unom = models.ForeignKey(House, on_delete=models.CASCADE, to_field='unom')
    district = models.IntegerField()
    material = models.IntegerField()
    purpose = models.IntegerField()
    house_class = models.IntegerField()
    event_cnt_cat = models.FloatField()
    floor_num = models.FloatField()
    flat_num = models.FloatField()
    square = models.FloatField()


class DataTemperature(models.Model):
    material = models.CharField(max_length=128)
    unom = models.ForeignKey(House, on_delete=models.CASCADE, to_field='unom')
