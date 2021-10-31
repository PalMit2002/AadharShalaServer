from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

import xml.etree.ElementTree as ET
import uuid
import requests
import json
import time
import os

from aadharshalaserver.server.models import Landlord, Tenant
from aadharshalaserver.server import serializers


@api_view(['GET'])
def update_server(request):
    os.system('git pull && systemctl restart uidai.service')
    return Response({'status': "Successfully Updated"})


@api_view(['POST'])
def genOTP(request):
    data = request.data
    aadharnum = data['username']
    token = str(uuid.uuid4())

    url = "https://stage1.uidai.gov.in/onlineekyc/getOtp/"

    payload = json.dumps({
        "uid": str(aadharnum),
        "txnId": token
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = json.loads(response.text)

    if(res['status'] == 'y' or res['status'] == 'Y'):
        return Response({'status': 'Y', 'token': token})

    return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['POST'])
def verOTP(request):
    data = request.data
    aadharnum = data['username']
    token = data['token']
    otp = data['otp']

    url = "https://stage1.uidai.gov.in/onlineekyc/getAuth/"

    payload = json.dumps({
        "uid": aadharnum,
        "txnId": token,
        "otp": otp
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = json.loads(response.text)

    if(res['status'] == 'y' or res['status'] == 'Y'):
        land, landc = Landlord.objects.get_or_create(aadharnum=aadharnum)
        ten, tenc = Tenant.objects.get_or_create(aadharnum=aadharnum)

        land.token = token
        ten.token = token

        t = time.time()

        land.time = t
        ten.time = t

        land.save()
        ten.save()

        return Response({'status': 'Y', 'token': token})

    return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['POST'])
def sendReqLandlord(request):
    data = request.data
    landAadharNum = data['landAadharNum']
    tenAadharNum = data['tenAadharNum']

    if(landAadharNum == tenAadharNum):
        return Response({'status': 'N', 'errCode': 'Landlord and Tenant cannot be the same'})

    ten = Tenant.objects.get(aadharnum=tenAadharNum)

    token = data['token']
    t = time.time()

    if ten.token == token and ten.time - t < 1800:

        land, lanc = Landlord.objects.get_or_create(
            aadharnum=landAadharNum)
        ten.landlord = land

        # Send notif to landlord

        return Response({'status': 'Y'})

    else:
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def verTenant(request):
    data = request.data
    landAadharNum = data['landAadharNum']
    tenAadharNum = data['tenAadharNum']

    land = Tenant.objects.get(aadharnum=landAadharNum)
    ten = Tenant.objects.get(aadharnum=tenAadharNum)

    if(ten.landlord != land):
        return Response({'status': 'N', 'errCode': 'Tenant is not Landlord'})

    token = data['token']
    otp = data['otp']

    url = "https://stage1.uidai.gov.in/onlineekyc/getEkyc/"

    payload = json.dumps({
        "uid": landAadharNum,
        "txnId": token,
        "otp": otp
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = json.loads(response.text)

    if(res['status'] == 'y' or res['status'] == 'Y'):
        xmlData = res['eKycString']
        resXml = ET.fromstring(xmlData)
        poa = resXml.find('UidData').find('Poa').attrib

        if('co' in poa):
            land.co = poa['co']
        if('house' in poa):
            land.house = poa['house']
        if('street' in poa):
            land.street = poa['street']
        if('lm' in poa):
            land.lm = poa['lm']
        if('loc' in poa):
            land.loc = poa['loc']
        if('vtc' in poa):
            land.vtc = poa['vtc']
        if('subdist' in poa):
            land.subdist = poa['subdist']
        if('dist' in poa):
            land.dist = poa['dist']
        if('state' in poa):
            land.state = poa['state']
        if('country' in poa):
            land.country = poa['country']
        if('pc' in poa):
            land.pc = poa['pc']
        if('po' in poa):
            land.po = poa['po']
        land.save()

        ten.isVerified = True
        ten.save()

        return Response({'status': 'Y'})

    else:
        return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['GET'])
def getLandTenants(request):
    reqData = request.data
    aadharnum = reqData['aadharnum']
    landlord = Landlord.objects.get(aadharnum=aadharnum)
    tenants = Tenant.objects.filter(landlord=landlord)
    tenants_ser = serializers.TenantSerializer(tenants, many=True)
    return Response({'status': 'Y', 'tenants': tenants_ser.data})


@api_view(['GET'])
def getLandAddr(request):
    data = request.data
    token = data['token']
    aadharnum = data['aadharnum']

    ten = Tenant.objects.get(aadharnum=aadharnum)

    t = time.time()

    if ten.token == token and ten.time - t < 1800:
        land = ten.landlord
        co = land.co
        house = land.house
        addr = land.street + ' ' + land.lm + ' ' + land.loc + ' ' + land.vtc + ' ' + land.subdist + \
            ' ' + land.dist + ' ' + land.state + ' ' + \
            land.country + ' ' + land.pc + ' ' + land.po

        return Response({'status': 'Y', 'co': co, 'house': house, 'addr': addr})
    else:
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def uptTenAddr(request):
    data = request.data
    token = data['token']
    aadharnum = data['aadharnum']

    ten = Tenant.objects.get(aadharnum=aadharnum)

    t = time.time()

    if ten.token == token and ten.time - t < 1800:
        co = data['co']
        house = data['house']

        ten.mod_co = co
        ten.mod_house = house

        ten.save()

        # Send updated address to aadhar

        return Response({'status': 'Y'})

    else:
        return Response({'status': 'N', 'errCode': 'Invalid Token'})
