from django.db import models
from django.contrib.auth.models import User
from equipment.models import Equipment

# Create your models here.


class Inquiry(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_on = models.DateTimeField()
    STATUS_CODES = (
        ('AQ', 'Awaiting Quotation'),
        ('AR', 'Awaiting Confirmation'),
        ('CO', 'Confirmed'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000)


class InquiryEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    inquiry = models.ManyToManyField(Inquiry)


class Quotation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE)
    STATUS_CODES = (
        ('PA', 'Accepted'),
        ('RE', 'Rejected'),
        ('AW', 'Awaiting Confirmation'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    created_on = models.DateTimeField()
    paid = models.BooleanField(default=False)
    transportation_cost = models.DecimalField(max_digits=12, decimal_places=2)
    comments = models.CharField(max_length=1000)


class QuotationEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    inquiry = models.ManyToManyField(Quotation)

