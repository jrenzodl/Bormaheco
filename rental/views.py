from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from equipment.models import Equipment
from django import template
from .models import Inquiry, InquiryEquipment, Quotation
from django.utils import timezone
from itertools import chain
from operator import attrgetter

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
    quotations = Quotation.objects.filter(inquiry__customer=loggedinuser)
    combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
    return render(request, 'transactions.html', {'transactions': combined_transactions})


def transactionsfiltered(request, transaction_type):
    loggedinuser = request.user
    if transaction_type == 'QU':
        quotations = Quotation.objects.filter(inquiry__customer=loggedinuser).order_by("-sent_on")
        return render(request, 'transactions.html', {'transactions': quotations, 'transaction_type': 'QU'})
    elif transaction_type == 'IN':
        inquiries = Inquiry.objects.filter(customer=loggedinuser).order_by("-sent_on")
        return render(request, 'transactions.html', {'transactions': inquiries, 'transaction_type': 'IN'})
    elif transaction_type == 'AL':
        inquiries = Inquiry.objects.filter(customer=loggedinuser)
        quotations = Quotation.objects.filter(inquiry__customer=loggedinuser)
        combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
        return render(request, 'transactions.html', {'transactions': combined_transactions})


def transactionitem(request, transaction_type, report, pk):
    loggedinuser = request.user
    pk = int(pk)
    if transaction_type == "AL":
        inquiries = Inquiry.objects.filter(customer=loggedinuser)
        quotations = Quotation.objects.filter(inquiry__customer=loggedinuser)
        combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
        if report == "QU":
            quotation = Quotation.objects.get(id=pk)
            return render(request, 'transactions.html', {'transactions': combined_transactions,
                                                         'transaction_type': transaction_type, 'details': quotation,
                                                         'index': pk})
        elif report == "IN":
            inquiry = Inquiry.objects.get(id=pk)
            return render(request, 'transactions.html',
                          {'transactions': combined_transactions, 'transaction_type': transaction_type,
                           'details': inquiry, 'index': pk})
    elif transaction_type == "QU":
        quotations = Quotation.objects.filter(inquiry__customer=loggedinuser).order_by("-sent_on")
        quotation = Quotation.objects.get(id=pk)
        return render(request, 'transactions.html',
                      {'transactions': quotations, 'transaction_type': transaction_type,
                       'details': quotation, 'index': pk})
    elif transaction_type == "IN":
        inquiries = Inquiry.objects.filter(customer=loggedinuser).order_by("-sent_on")
        inquiry = Inquiry.objects.get(id=pk)
        return render(request, 'transactions.html',
                      {'transactions': inquiries, 'transaction_type': transaction_type, 'details': inquiry,
                       'index': pk})


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


def confirmpayment(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation.paid = True
    quotation.save()
    return redirect('rental:getitem', transaction_type="QU", report="QU", pk=pk)
