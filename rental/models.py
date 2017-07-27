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
        ('RE', 'Rejected'))
    status = models.CharField(max_length=2, choices=STATUS_CODES)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    comments = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return '{}:{} - {}'.format(self.get_status_display(), self.customer.username, self.sent_on)

    def related_quotation(self):
        if self.quotation:
            return self.quotation
        else:
            return 'null'

    def getallequipment(self):
        return self.inquiryequipment_set.all()

    def has_conflict(self):
        list_of_equipment = self.inquiryequipment_set.all()
        for list_of_equipment in list_of_equipment:
            result = list_of_equipment.equipment.checkconflict(self.id)
            if result is True:
                return True

        return False


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
    sent_on = models.DateTimeField()
    paid = models.BooleanField(default=False)
    transportation_cost = models.DecimalField(max_digits=12, decimal_places=2)
    comments = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return '{}:{} - {}'.format(self.get_status_display(), self.created_by.username, self.sent_on)

    def getprice(self):
        equipment = self.quotationequipment_set
        totalprice = 0
        date = self.inquiry.end_date - self.inquiry.start_date
        date = (date.days + 1) * 24
        for unit in equipment.all():
            totalprice += unit.equipment.hourly_service_rate
        totalprice = totalprice * date
        return totalprice + self.transportation_cost

    def gettotalrental(self):
        equipment = self.quotationequipment_set
        totalprice = 0
        for unit in equipment.all():
            totalprice += unit.equipment.hourly_service_rate
        return totalprice

    def getallequipment(self):
        return self.quotationequipment_set.all()


class QuotationEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{} - {}: {}'.format(self.quotation.get_status_display(), self.quotation.created_by.username,
                                       self.quotation.sent_on, self.equipment.name)
