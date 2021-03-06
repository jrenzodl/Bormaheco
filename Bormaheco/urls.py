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
from accounts import views
from django.contrib.auth.views import logout
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [

    url(r'^admin/', admin.site.urls, name='administration'),

    url(r'^equipment/', include('equipment.urls'), name='equipment'),

    url(r'^rental/', include('rental.urls'), name='rental'),

    url(r'^logout/', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),

    url(r'^logincheckout/', views.login_user_checkout, name='checkout_login'),

    url(r'^register/', views.reqister, name='register'),

    url(r'^login/', views.login_user, name='login'),

    url(r'^checkuser/', views.check_username, name='usercheck'),

    url(r'^$', views.homepage, name='mainpage'),

    url(r'^error/', TemplateView.as_view(template_name='notallowed.html'), name='errorpage'),
]

admin.site.site_header = "Bormaheco Administration"
admin.site.site_title = "Bormaheco Inc. | Admin"
