from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from equipment.models import Equipment
from django import template
from .models import Inquiry, InquiryEquipment
from django.utils import timezone

# Create your views here.


def checkout(request):
    return render(request, 'checkout.html')


def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])
    if item_id in cart:
        return redirect('equipment:mainpage')
    else:
        cart.append(item_id)
        request.session['cart'] = cart
        return redirect('equipment:mainpage')


def delete_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    cart.remove(item_id)
    request.session['cart'] = cart
    return redirect('equipment:mainpage')


def transactions(request):
    loggedinuser = request.user
    inquiries = Inquiry.objects.filter(customer=loggedinuser)
    return render(request, 'transactions.html', {'inquiries': inquiries})


def checkout_cart(request):
    location = request.POST.get("location")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    comments = request.POST.get("comments")
    datetimenow = timezone.now()
    user = request.user
    inquiry = Inquiry(location=location, end_date=enddate, sent_on=datetimenow, start_date=startdate,
                      comments=comments, customer=user, status="AQ")
    inquiry.save()

    cart = request.session.get('cart', [])
    equipment = Equipment.objects.filter(id__in=cart)
    for unit in equipment:
        inquiryequipment = InquiryEquipment(equipment=unit, inquiry=inquiry)
        inquiryequipment.save()

    request.session['cart'] = []
    return redirect("rental:transactions")
