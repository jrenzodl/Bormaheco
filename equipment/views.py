from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
from accounts.models import User, UserAccount
from . import models
import json
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from rental.models import Inquiry

# Create your views here.


def equipment_index(request):
    list_of_equipment = Equipment.objects.order_by('name')
    user = request.user
    if user.is_anonymous or user.is_superuser:
        return render(request, 'equipments.html', {'equipment': list_of_equipment})
    else:
        useraccount = UserAccount.objects.get(user=user)
        if useraccount.user_type == "MM":
            list_of_maintenance = MaintenanceTransaction.objects.order_by('-start_date')
            needsmaintenance = Equipment.objects.filter(hours_worked__gte=300)
            undermaintenance = Equipment.objects.filter(status="UM")
            equipment = Equipment.objects.filter(status="AV").filter(hours_worked__lt=300)
            return render(request, 'maintenanceequipment.html', {'equipment': needsmaintenance,
                                                                 'maintenance': list_of_maintenance,
                                                                 'undermaintenance': undermaintenance,
                                                                 'normal': equipment})
        elif useraccount.user_type == "EM":
            return render(request, 'emequipments.html', {'equipment': list_of_equipment})
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


def get_em_equipment(request, pk):
    list_of_equipment = Equipment.objects.order_by('name')
    unit = Equipment.objects.get(id=pk)
    return render(request, 'emequipments.html', {'equipment': list_of_equipment, 'unit':unit})


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


def start_maintenance(request, primary_key):
    equipment = Equipment.objects.get(id=primary_key)
    unfinishedmaintenance = MaintenanceTransaction(equipment=equipment, start_date=timezone.now())
    equipment.hours_worked = 0
    equipment.status = "UM"
    equipment.save()
    unfinishedmaintenance.save()
    return redirect("equipment:mainpage")


def end_maintenance(request):
    primary_key = request.POST.get('id')
    equipment = Equipment.objects.get(id=primary_key)
    equipment.status = 'AV'
    equipment.save()
    latest_maintenance = MaintenanceTransaction.objects.filter(equipment=equipment).latest("start_date")
    latest_maintenance.end_date = timezone.now()
    latest_maintenance.cost = request.POST.get('cost')
    latest_maintenance.save()
    return redirect("equipment:mainpage")


def dispatch(request, pk):
    equipment = Equipment.objects.get(id=pk)
    inquiries = Inquiry.objects.filter(inquiryequipment__equipment=equipment).filter(start_date__lte=timezone.now()). \
        filter(end_date__gte=timezone.now()).filter(status="CO").get()
    date = inquiries.end_date - inquiries.start_date
    date = (date.days + 1) * 24
    equipment.status = "IE"
    equipment.hours_worked = equipment.hours_worked + date
    equipment.save()
    return redirect("equipment:mainpage")


def recall(request, pk):
    equipment = Equipment.objects.get(id=pk)
    equipment.status = "AV"
    equipment.save()
    return redirect("equipment:mainpage")
