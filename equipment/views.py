from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
from .forms import EquipmentForm
from . import models
import json

# Create your views here.


def equipment_index(request):
    list_of_equipment = Equipment.objects.order_by('name')
    return render(request, 'equipments.html', {'equipment': list_of_equipment})


def filter_equipment(request, types):
    if types == "AL":
        list_of_equipment = Equipment.objects.order_by('name')
    else:
        list_of_equipment = Equipment.objects.filter(type=types)

    return render(request, 'equipments.html', {'equipment': list_of_equipment, 'types': types})


def add_equipment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        acquisition_cost = request.POST.get('acquisition_cost')
        details = request.POST.get('details')
        eq_type = request.POST.get('type')
        hourly_service_rate = request.POST.get('hourly_service_rate')
        image = request.FILES.get('image')
        acquisition_date = request.POST.get('acquisition_date')
        status = request.POST.get('status')
        equipment = Equipment(name=name, brand=brand, acquisition_cost=acquisition_cost,
                              details=details, hourly_service_rate=hourly_service_rate,
                              image=image, acquisition_date=acquisition_date,
                              status=status, type=eq_type)
        equipment.save()

        return HttpResponse("success")
