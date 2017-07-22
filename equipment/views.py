from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
from accounts.models import User, UserAccount
from . import models
import json
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def equipment_index(request):
    list_of_equipment = Equipment.objects.order_by('name')
    user = request.user
    if user.is_anonymous or user.is_superuser:
        return render(request, 'equipments.html', {'equipment': list_of_equipment})
    else:
        useraccount = UserAccount.objects.get(user=user)
        if useraccount.user_type == "MM":
            return render(request, 'maintenanceequipment.html', {'equipment': list_of_equipment})
        else:
            return render(request, 'equipments.html', {'equipment': list_of_equipment})


@user_passes_test(lambda u: u.is_superuser, login_url='equipment:mainpage')
def delete_equipment(request, primary_key):
    equipment = Equipment.objects.filter(id=primary_key)
    equipment.delete()
    return redirect('equipment:mainpage')


def get_equipment(request, eqid):
    equipment = Equipment.objects.filter(id=eqid)
    return HttpResponse(equipment)


def filter_equipment(request, types):
    if types == "AL":
        list_of_equipment = Equipment.objects.order_by('name')
    else:
        list_of_equipment = Equipment.objects.filter(type=types)

    return render(request, 'equipments.html', {'equipment': list_of_equipment, 'types': types})


@user_passes_test(lambda u: u.is_superuser, login_url='equipment:mainpage')
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
