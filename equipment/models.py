from django.db import models

# Create your models here.


class Equipment(models.Model):
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2)
    acquisition_date = models.DateField()
    details = models.CharField(max_length=2000)
    TYPE_CODES = (
        ('EX', 'Excavator'),
        ('BL', 'Backhoe Loader'),
        ('BR', 'Breaker'),
        ('SL', 'Skidsteer Loader'),
        ('RR', 'Road Roller'),
        ('RG', 'Road Grader'),
        ('PL', 'Payloader'),
        ('BD', 'Bulldozer'),
        ('CR', 'Crane'),
        ('AC', 'Air Compressor'),
        ('GS', 'Genarating Sets'),
        ('FL', 'Forklifts'),
        ('FT', 'Flatebed Trucks'),
        ('DT', 'Dump Truck'),
        ('LB', 'Low Bed Trailer'),
        ('PM', 'Prime Mover'),
        ('MT', 'Manlift Trucks'),
        ('MC', 'Motorcycles'),
        ('OT', 'Other'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CODES)
    STATUS_CODES = (
        ('IE', 'In Engagement'),
        ('AV', 'Available'),
        ('UM', 'Under Maintenance'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    hourly_service_rate = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="equipmentimages", default='../static/images/defaultequipment.png')

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)


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
