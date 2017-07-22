import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.models import UserAccount
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from rental.models import Inquiry, InquiryEquipment
from equipment.models import Equipment
from django.urls import reverse
from rental.views import transactions
from django.utils import timezone

# Create your views here.


def homepage(request):
    return render(request, 'mainpage.html')


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def reqister(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    company = request.POST.get("company")
    location = request.POST.get("location")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    comments = request.POST.get("comments")
    datetimenow = timezone.now()

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    userdetails = UserAccount(user=user, user_type='CU', company=company)
    userdetails.save()
    login(request, user)

    inquiry = Inquiry(location=location, start_date=startdate, end_date=enddate, sent_on=datetimenow,
                      comments=comments, customer=user, status="AQ")
    inquiry.save()

    cart = request.session.get('cart', [])
    equipment = Equipment.objects.filter(id__in=cart)
    for unit in equipment:
        inquiryequipment = InquiryEquipment(equipment=unit, inquiry=inquiry)
        inquiryequipment.save()

    request.session['cart'] = []
    return HttpResponse('1')


def check_username(request):
    username = request.POST.get("username")

    if User.objects.filter(username=username).exists():
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def login_user_checkout(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    location = request.POST.get("location")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    comments = request.POST.get("comments")
    datetimenow = timezone.now()
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        inquiry = Inquiry(location=location, start_date=startdate, end_date=enddate, sent_on=datetimenow,
                          comments=comments, customer=user, status="AQ")
        inquiry.save()

        cart = request.session.get('cart', [])
        equipment = Equipment.objects.filter(id__in=cart)
        for unit in equipment:
            inquiryequipment = InquiryEquipment(equipment=unit, inquiry=inquiry)
            inquiryequipment.save()

        request.session['cart'] = []
        return HttpResponse(True)
    else:
        return HttpResponse(False)
