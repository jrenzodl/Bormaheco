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

    def __str__(self):
        return '{}:{} - {}'.format(self.get_status_display(), self.customer.username, self.sent_on)


class InquiryEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{} - {}: {}'.format(self.inquiry.get_status_display(), self.inquiry.customer.username,
                                       self.inquiry.sent_on, self.equipment.name)


class Quotation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE)
    STATUS_CODES = (
        ('PA', 'Accepted'),
        ('RE', 'Rejected'),
        ('AW', 'Awaiting Confirmation'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    created_on = models.DateTimeField()
    paid = models.BooleanField(default=False)
    transportation_cost = models.DecimalField(max_digits=12, decimal_places=2)
    comments = models.CharField(max_length=1000)

    def __str__(self):
        return '{}:{} - {}'.format(self.get_status_display(), self.created_by.username, self.created_on)


class QuotationEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{} - {}: {}'.format(self.quotation.get_status_display(), self.quotation.created_by.username,
                                       self.quotation.created_on, self.equipment.name)
