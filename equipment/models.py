from django.db import models

# Create your models here.


class Equipment(models.Model):
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2)
    acquisition_date = models.DateField()
    details = models.CharField(max_length=2000)
    STATUS_CODES = (
        ('IE', 'In Engagement'),
        ('AV', 'Available'),
        ('UM', 'Under Maintenance'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    hourly_service_rate = models.DecimalField(max_digits=12, decimal_places=2)
    equipment_type = models.CharField(max_length=20)


class EquipmentEngagement(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
