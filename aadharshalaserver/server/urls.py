"""aadharshalaserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from aadharshalaserver.server import views


urlpatterns = [
    path('check_token/', views.checkToken),
    path('gen_otp/', views.genOTP),
    path('ver_otp/', views.verOTP),
    path('send_req_land/', views.sendReqLandlord),
    path('ver_tenant/', views.verTenant),
    path('get_landlord_tenants/', views.getLandTenants),
    path('get_landlord_address/', views.getLandAddr),
    path('upt_tenant_addr/', views.uptTenAddr),

    path('reduce_addr/', views.reduceAddr),

    path('update_server', views.update_server),
]
