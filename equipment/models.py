from django.db import models
from django.utils import timezone
from itertools import chain
from operator import attrgetter

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
        ('FT', 'Flatbed Truck'),
        ('FL', 'Forklifts'),
        ('GS', 'Genarating Set'),
        ('LB', 'Low Bed Trailer'),
        ('MT', 'Manlift Truck'),
        ('MC', 'Motorcycle'),
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
        ('UM', 'Under Maintenance'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    hours_worked = models.IntegerField(default=0)
    total_hours_worked = models.IntegerField(default=0)
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
            'type': self.get_type_display,
            'status': self.status,
            'hourly_service_rate': self.hourly_service_rate,
            'imageurl': self.image.url,
        }

    def checkconflict(self, index):
        from rental.models import Inquiry
        inquiry2 = Inquiry.objects.get(id=index)
        inquiries = self.inquiryequipment_set.all().exclude(inquiry_id=index)
        if self.status == "UM":
            return True

        if inquiry2.status == "AQ":
            for inquiryequipment in inquiries:
                if inquiryequipment.inquiry.status == "CO":
                    test_start = inquiryequipment.inquiry.start_date
                    test_end = inquiryequipment.inquiry.end_date
                    if test_start <= inquiry2.start_date <= test_end:
                        return True
                    if test_start <= inquiry2.end_date <= test_end:
                        return True

        return False

    def has_engagement(self):
        from rental.models import Inquiry
        inquiries = Inquiry.objects.filter(inquiryequipment__equipment=self).filter(start_date__lte=timezone.now()).\
            filter(end_date__gte=timezone.now()).filter(status="CO")
        if not inquiries:
            return False
        else:
            return True

    def get_previous_transactions(self):
        from rental.models import Inquiry
        inquiries = Inquiry.objects.filter(inquiryequipment__equipment=self).filter(end_date__lt=timezone.now()).\
            filter(status="CO")
        maintenance = MaintenanceTransaction.objects.filter(equipment=self).filter(end_date__lt=timezone.now())
        combined = sorted(chain(inquiries, maintenance), key=attrgetter('end_date'), reverse=True)
        return combined

    def get_roi(self):
        from rental.models import Quotation
        quotation = Quotation.objects.filter(quotationequipment__equipment=self).filter(paid=True).filter(status="PA")
        income = 0
        for x in quotation:
            days = x.inquiry.end_date - x.inquiry.start_date
            days = (days.days + 1) * 24
            income = income + (days * self.hourly_service_rate)

        maintenance = MaintenanceTransaction.objects.filter(equipment=self).filter(end_date__lte=timezone.now())
        maintenance_cost = 0
        for y in maintenance:
            maintenance_cost = maintenance_cost + y.cost

        roi = (income - (maintenance_cost + self.acquisition_cost))/(maintenance_cost + self.acquisition_cost)

        return roi


# WAG TO
#
#    class EquipmentEngagement(models.Model):
#       equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
#        date = models.DateField()
#        start_time = models.TimeField()
#        end_time = models.TimeField()
#
#        def __str__(self):
#            return '{}, {}'.format(self.equipment.name, self.date)


class MaintenanceTransaction(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def __str__(self):
        return '{}, {}'.format(self.equipment.name, self.start_date)
