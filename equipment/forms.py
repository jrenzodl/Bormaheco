from django.forms import ModelForm
from django import forms
from equipment.models import Equipment


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ['brand', 'name', 'acquisition_date', 'acquisition_cost', 'details', 'type', 'status',
                  'hourly_service_rate', 'image']

