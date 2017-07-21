import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.models import UserAccount
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rental.models import Inquiry, InquiryEquipment
from equipment.models import Equipment

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
    password = make_password(request.POST.get("password"))
    email = request.POST.get("email")
    company = request.POST.get("company")
    location = request.POST.get("location")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    comments = request.POST.get("comments")
    datetimenow = datetime.datetime.now()

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
        inquiryequipment = InquiryEquipment()
        inquiryequipment.equipment = unit
        inquiryequipment.save()
        inquiryequipment.inquiry.add(inquiry)

    return redirect('rental:transactions')


def check_username(request):
    username = request.POST.get("username")
    user = User.objects.filter(username=username)
    if user is not None:
        return HttpResponse(False)
    else:
        return HttpResponse(True)


def login_user_checkout(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(True)
    else:
        return HttpResponse(False)
