"""Bormaheco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from . import views
from django.views.generic import TemplateView
app_name = 'rental'
urlpatterns = [

    url(r'^checkout_cart/', views.checkout_cart, name='checkout_cart'),

    url(r'^transactions/(?P<transaction_type>\D\D)$', views.transactionsfiltered, name='filtered_transactions'),

    url(r'^transactions/(?P<transaction_type>\D\D)/(?P<report>\D\D)/(?P<pk>\d+)', views.transactionitem,
        name='getitem'),

    url(r'^confirmpayment/(?P<pk>\d+)', views.confirmpayment, name='confirmpayment'),

    url(r'^transactions/$', views.transactions, name='transactions'),

    url(r'^checkout/', views.checkout, name='checkout'),

    url(r'^deletefromcart/(?P<item_id>\d+)', views.delete_from_cart, name='delete_from_cart'),

    url(r'^addtocart/(?P<item_id>\d+)', views.add_to_cart, name='addtocart'),
]
