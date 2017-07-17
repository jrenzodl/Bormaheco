from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json

# Create your views here.


def get_cart(request):
    cart = request.session.get('cart', {})
    if len(cart) == 0:
        return HttpResponse("0")
    else:
        return HttpResponse(json.dumps(cart))
