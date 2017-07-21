from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    company = models.CharField(max_length=50)
    USER_TYPE_CHOICES = (
        ('FI', 'Finance'),
        ('EM', 'Equipment Manager'),
        ('MM', 'Maintenance Manager'),
        ('CU', 'Customer'))
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)
