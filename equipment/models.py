from django.db import models

# Create your models here.


class Equipment(models.Model):
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2)
    acquisition_date = models.DateField()
    details = models.CharField(max_length=2000)
    TYPE_CODES = (
        ('AC', 'Air Compressor'),
        ('BL', 'Backhoe Loader'),
        ('BR', 'Breaker'),
        ('BD', 'Bulldozer'),
        ('CR', 'Crane'),
        ('DT', 'Dump Truck'),
        ('EX', 'Excavator'),
        ('FT', 'Flatbed Trucks'),
        ('FL', 'Forklifts'),
        ('GS', 'Genarating Sets'),
        ('LB', 'Low Bed Trailer'),
        ('MT', 'Manlift Trucks'),
        ('MC', 'Motorcycles'),
        ('PL', 'Payloader'),
        ('PM', 'Prime Mover'),
        ('RG', 'Road Grader'),
        ('RR', 'Road Roller'),
        ('SL', 'Skidsteer Loader'),
        ('OT', 'Other'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CODES)
    STATUS_CODES = (
        ('IE', 'In Engagement'),
        ('AV', 'Available'),
        ('UM', 'Under Maintenance'),
        ('US', 'Unserviceable'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    hourly_service_rate = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="equipmentimages", default='../media/equipmentimages/defaultequipment.png')

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)

    def as_dict(self):
        return {
            'brand': self.brand,
            'name': self.name,
            'acquisitioncost': self.acquisition_cost,
            'acquisitiondate': self.acquisition_date,
            'details': self.details,
            'type': self.type,
            'status': self.status,
            'hourly_service_rate': self.hourly_service_rate,
            'imageurl': self.image.url,
        }


class EquipmentEngagement(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '{}, {}'.format(self.equipment.name, self.date)


class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return '{}, {}'.format(self.equipment.name, self.maintenance_date)
