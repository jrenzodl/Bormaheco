from django.shortcuts import render
from .models import *

# Create your views here.


def equipment_index(request):
    list_of_equipment = Equipment.objects.order_by('name')
    return render(request, 'equipments.html', {'equipment': list_of_equipment})
