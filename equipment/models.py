from django.db import models

# Create your models here.


class Equipment(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    unitprice = models.DecimalField(max_digits=12, decimal_places=2)
    dateacquired = models.DateField()
    propertynumber = models.CharField(max_length=50)
    serialnumber = models.CharField(max_length=50)
    remarks = models.CharField(max_length=500)

