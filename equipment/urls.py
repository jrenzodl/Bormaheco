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

    url(r'^equipmentdetails(?P<pk>\d+)', views.get_em_equipment, name='getemequipment'),

    url(r'^dispatch/(?P<pk>\d+)', views.dispatch, name='dispatch'),

    url(r'^recall/(?P<pk>\d+)', views.recall, name='recall'),

    url(r'^end_maintenance/', views.end_maintenance, name='end_maintenance'),

    url(r'^start_maintenance/(?P<primary_key>\d+)', views.start_maintenance, name='start_maintenance'),

    url(r'^deleteequipment/(?P<primary_key>\d+)', views.delete_equipment, name='deleteequipment'),

    url(r'^filterequipment/(?P<types>\D\D)/', views.filter_equipment, name='filterequipment'),

    url(r'^addequipment/', views.add_equipment, name='addequipment'),

    url(r'^getequipment/(?P<eqid>\d+)', views.get_equipment, name='getequipment')
]
