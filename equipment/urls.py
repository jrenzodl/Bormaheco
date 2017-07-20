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
from . import views
from django.contrib.auth.views import logout
from django.conf import settings
app_name = 'equipment'
urlpatterns = [
    url(r'^$', views.equipment_index, name='mainpage'),

    url(r'^deleteequipment/(?P<primary_key>\d+)', views.delete_equipment, name='deleteequipment'),

    url(r'^filterequipment/(?P<types>\D\D)/', views.filter_equipment, name='filterequipment'),

    url(r'^addequipment/', views.add_equipment, name='addequipment'),
]
