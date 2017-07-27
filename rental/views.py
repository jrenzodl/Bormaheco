from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from equipment.models import Equipment
from django import template
from .models import Inquiry, InquiryEquipment, Quotation, QuotationEquipment
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


@user_passes_test(lambda u: u.is_anonymous or (u.useraccount.user_type != "MM" and u.useraccount.user_type != "FI" and
                  u.useraccount.user_type != "EM" and u.is_superuser is False), login_url='errorpage')
def checkout(request):
    return render(request, 'checkout.html')


@user_passes_test(lambda u: u.is_anonymous or (u.useraccount.user_type != "MM" and u.useraccount.user_type != "FI" and
                  u.useraccount.user_type != "EM" and u.is_superuser is False), login_url='errorpage')
def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])
    if item_id in cart:
        return redirect('equipment:mainpage')
    else:
        cart.append(item_id)
        request.session['cart'] = cart
        return redirect('equipment:mainpage')


@user_passes_test(lambda u: u.is_anonymous or (u.useraccount.user_type != "MM" and u.useraccount.user_type != "FI" and
                  u.useraccount.user_type != "EM" and u.is_superuser is False), login_url='errorpage')
def delete_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    cart.remove(item_id)
    request.session['cart'] = cart
    return redirect('equipment:mainpage')


@user_passes_test(lambda u: u.is_anonymous() is False, login_url='errorpage')
def transactions(request):
    loggedinuser = request.user
    if loggedinuser.useraccount.user_type == "CU":
        inquiries = Inquiry.objects.filter(customer=loggedinuser)
        quotations = Quotation.objects.filter(inquiry__customer=loggedinuser)
        combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
        return render(request, 'transactions.html', {'transactions': combined_transactions, 'transaction_type': "AL"})
    elif loggedinuser.useraccount.user_type == "EM":
        inquiries = Inquiry.objects.all()
        quotations = Quotation.objects.all()
        combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
        return render(request, 'transactions.html', {'transactions': combined_transactions, 'transaction_type': "AL"})
    elif loggedinuser.useraccount.user_type == "FI":
        quotations = Quotation.objects.all().order_by('-sent_on')
        return render(request, 'finance.html', {'quotations': quotations})
    else:
        return redirect('errorpage')


@user_passes_test(lambda u: u.is_anonymous() is False, login_url='errorpage')
def transactionsfiltered(request, transaction_type):
    loggedinuser = request.user
    if loggedinuser.useraccount.user_type == "CU":
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
            return render(request, 'transactions.html', {'transactions': combined_transactions,
                                                         'transaction_type': 'AL'})
    elif loggedinuser.useraccount.user_type == "EM":
        if transaction_type == 'QU':
            quotations = Quotation.objects.order_by("-sent_on").all()
            return render(request, 'transactions.html', {'transactions': quotations, 'transaction_type': 'QU'})
        elif transaction_type == 'IN':
            inquiries = Inquiry.objects.order_by("-sent_on").all()
            return render(request, 'transactions.html', {'transactions': inquiries, 'transaction_type': 'IN'})
        elif transaction_type == 'AL':
            inquiries = Inquiry.objects.all()
            quotations = Quotation.objects.all()
            combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
            return render(request, 'transactions.html', {'transactions': combined_transactions,
                                                         'transaction_type': 'AL'})
    else:
        return redirect('errorpage')


@user_passes_test(lambda u: u.is_anonymous() is False, login_url='errorpage')
def transactionitem(request, transaction_type, report, pk):
    allequipment = Equipment.objects.all()
    loggedinuser = request.user
    pk = int(pk)
    if loggedinuser.useraccount.user_type == "CU":
        if transaction_type == "AL":
            inquiries = Inquiry.objects.filter(customer=loggedinuser)
            quotations = Quotation.objects.filter(inquiry__customer=loggedinuser)
            combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
            if report == "QU":
                quotation = Quotation.objects.get(id=pk)
                return render(request, 'transactions.html', {'transactions': combined_transactions,
                                                             'transaction_type': transaction_type, 'details': quotation,
                                                             'index': pk, 'equipment': allequipment})
            elif report == "IN":
                inquiry = Inquiry.objects.get(id=pk)
                return render(request, 'transactions.html',
                              {'transactions': combined_transactions, 'transaction_type': transaction_type,
                               'details': inquiry, 'index': pk, 'equipment': allequipment})
        elif transaction_type == "QU":
            quotations = Quotation.objects.filter(inquiry__customer=loggedinuser).order_by("-sent_on")
            quotation = Quotation.objects.get(id=pk)
            return render(request, 'transactions.html',
                          {'transactions': quotations, 'transaction_type': transaction_type,
                           'details': quotation, 'index': pk, 'equipment': allequipment})
        elif transaction_type == "IN":
            inquiries = Inquiry.objects.filter(customer=loggedinuser).order_by("-sent_on")
            inquiry = Inquiry.objects.get(id=pk)
            return render(request, 'transactions.html',
                          {'transactions': inquiries, 'transaction_type': transaction_type, 'details': inquiry,
                           'index': pk, 'equipment': allequipment})
    elif loggedinuser.useraccount.user_type == "EM":
        if transaction_type == "AL":
            inquiries = Inquiry.objects.all()
            quotations = Quotation.objects.all()
            combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
            if report == "QU":
                quotation = Quotation.objects.get(id=pk)
                return render(request, 'transactions.html', {'transactions': combined_transactions,
                                                             'transaction_type': transaction_type, 'details': quotation,
                                                             'index': pk, 'equipment': allequipment})
            elif report == "IN":
                inquiry = Inquiry.objects.get(id=pk)
                return render(request, 'transactions.html',
                              {'transactions': combined_transactions, 'transaction_type': transaction_type,
                               'details': inquiry, 'index': pk, 'equipment': allequipment})
        elif transaction_type == "QU":
            quotations = Quotation.objects.order_by("-sent_on").all()
            quotation = Quotation.objects.get(id=pk)
            return render(request, 'transactions.html',
                          {'transactions': quotations, 'transaction_type': transaction_type,
                           'details': quotation, 'index': pk, 'equipment': allequipment})
        elif transaction_type == "IN":
            inquiries = Inquiry.objects.order_by("-sent_on").all()
            inquiry = Inquiry.objects.get(id=pk)
            return render(request, 'transactions.html',
                          {'transactions': inquiries, 'transaction_type': transaction_type, 'details': inquiry,
                           'index': pk, 'equipment': allequipment})
    else:
        return redirect('errorpage')


@user_passes_test(lambda u: u.is_anonymous or (u.useraccount.user_type != "MM" and u.useraccount.user_type != "FI" and
                  u.useraccount.user_type != "EM" and u.is_superuser is False), login_url='errorpage')
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


@user_passes_test(lambda u: u.useraccount.user_type == "CU", login_url='errorpage')
def confirmpayment(request, pk):
    quotation = Quotation.objects.get(id=pk)
    if quotation.inquiry.customer == request.user:
        quotation.paid = True
        quotation.save()
        return redirect('rental:getitem', transaction_type="QU", report="QU", pk=pk)
    else:
        return redirect('errorpage')


@user_passes_test(lambda u: u.useraccount.user_type == "EM", login_url='errorpage')
def create_quotation(request):
    cost = request.POST.get("cost")
    inquiryid = int(request.POST.get('inquiryid'))
    listofequipment = request.POST.getlist('listofequipment[]')
    comments = request.POST.get('comments')
    inquiry = Inquiry.objects.get(id=inquiryid)
    inquiry.status = "AR"
    inquiry.save()
    quotation = Quotation()
    quotation.created_by = request.user
    quotation.inquiry = inquiry
    quotation.transportation_cost = cost
    quotation.comments = comments
    quotation.sent_on = timezone.now()
    quotation.status = "AW"
    quotation.save()

    for x in listofequipment:
        equipment = Equipment.objects.get(id=x)
        qe = QuotationEquipment(equipment=equipment, quotation=quotation)
        qe.save()

    return HttpResponse(True)


@user_passes_test(lambda u: u.useraccount.user_type == "EM", login_url='errorpage')
def reject_inquiry(request, pk):
    inquiry = Inquiry.objects.get(id=pk)
    inquiry.status = "RE"
    inquiry.save()
    inquiries = Inquiry.objects.all()
    quotations = Quotation.objects.all()
    combined_transactions = sorted(chain(inquiries, quotations), key=attrgetter('sent_on'), reverse=True)
    return render(request, 'transactions.html', {'transactions': combined_transactions, 'transaction_type': "AL"})


@user_passes_test(lambda u: u.useraccount.user_type == "FI", login_url='errorpage')
def confirm_payment_finance(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation.status = "PA"
    quotation.save()
    inquiry = quotation.inquiry
    inquiry.status = "CO"
    inquiry.save()
    return redirect('rental:transactions')

