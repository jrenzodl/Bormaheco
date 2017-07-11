from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Inquiry)

admin.site.register(InquiryEquipment)

admin.site.register(Quotation)

admin.site.register(QuotationEquipment)