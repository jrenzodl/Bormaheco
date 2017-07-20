from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from equipment.models import Equipment
from django import template

# Create your views here.


def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])

    cart.append(item_id)
    request.session['cart'] = cart
    return redirect('equipment:mainpage')
