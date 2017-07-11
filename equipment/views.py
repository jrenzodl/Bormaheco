from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
import json

# Create your views here.


def equipment_index(request):
    list_of_equipment = Equipment.objects.order_by('name')
    return render(request, 'equipments.html', {'equipment': list_of_equipment})


def filter_equipment(request, types):
    list_of_equipment = Equipment.objects.filter(type=types)
    list_of_equipment = serializers.serialize('json', list_of_equipment)
    return HttpResponse(list_of_equipment, content_type="application/json")
