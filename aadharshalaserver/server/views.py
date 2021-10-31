from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

import xml.etree.ElementTree as ET
import uuid
import requests
import json
import time
import os
import random
from cryptography.fernet import Fernet

from aadharshalaserver.server.address_UIDAI import new_address

from aadharshalaserver.server.models import Landlord, Log, Tenant
from aadharshalaserver.server import serializers


def createLog(event, msg="", initiator=""):
    Log.objects.create(event=event, msg=msg, initiator=initiator)


def encrypt(s):
    message = "my deep dark secret".encode()
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted


@api_view(['POST'])
def checkToken(request):
    data = request.data
    token = data['token']
    try:

        ten = Tenant.objects.get(token=token)
        t = time.time()
        if ten.token == token and abs(ten.time - t) < 1800:
            createLog("Token checked and is valid",
                      initiator=encrypt(ten.aadharnum))
            return Response({'status': 'Y'})
        else:
            createLog("Token has expired", initiator=encrypt(ten.aadharnum))
            return Response({'status': 'N'})

    except:
        createLog("No user found for token")
        return Response({'status': 'N'})


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
        land, landc = Landlord.objects.get_or_create(aadharnum=aadharnum)
        ten, tenc = Tenant.objects.get_or_create(aadharnum=aadharnum)

        land.token = token
        ten.token = token

        land.time = None
        ten.time = None

        land.save()
        ten.save()

        createLog("OTP generated")

        return Response({'status': 'Y', 'token': token, 'errCode': res['errCode']})

    createLog("OTP generation failed")
    return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['POST'])
def verOTP(request):
    data = request.data

    token = data['token']
    otp = data['otp']

    ten = Tenant.objects.get(token=token)
    aadharnum = ten.aadharnum

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
        land = Landlord.objects.get(aadharnum=aadharnum)
        ten = Tenant.objects.get(aadharnum=aadharnum)

        token = uuid.uuid4()

        land.token = token
        ten.token = token

        t = time.time()

        land.time = t
        ten.time = t

        land.save()
        ten.save()

        createLog("OTP verified")

        return Response({'status': 'Y', 'token': token, 'errCode': res['errCode']})

    createLog("OTP verification failed")
    return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['POST'])
def sendReqLandlord(request):
    data = request.data
    landAadharNum = data['landAadharNum']

    token = data['token']

    ten = Tenant.objects.get(token=token)

    tenAadharNum = ten.aadharnum

    if(landAadharNum == tenAadharNum):
        createLog("Request Sent to Landlord failed",
                  initiator=encrypt(tenAadharNum))
        return Response({'status': 'N', 'errCode': 'Landlord and Tenant cannot be the same'})

    t = time.time()

    if ten.token == token and ten.time - t < 1800:

        land, lanc = Landlord.objects.get_or_create(
            aadharnum=landAadharNum)
        ten.landlord = land

        reqCode = str(random.randint(1, 9999))
        ten.reqCode = reqCode

        ten.save()

        # Send notif to landlord

        createLog("Request sent to landlord", initiator=encrypt(tenAadharNum))
        return Response({'status': 'Y', 'reqCode': reqCode})

    else:
        createLog("Request sent to landlord failed",
                  initiator=encrypt(tenAadharNum))
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def verTenant(request):
    data = request.data
    token = data['token']
    reqCode = data['reqCode']

    land = Landlord.objects.get(token=token)
    ten = Tenant.objects.get(reqCode=reqCode)

    landAadharNum = land.aadharnum

    if(ten.landlord.aadharnum != landAadharNum):
        createLog("Verification of tenant failed due to invalid landlord",
                  initiator=encrypt(landAadharNum))
        return Response({'status': 'N', 'errCode': 'Tenant is not of Landlord'})

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

        createLog("Tenant verified", initiator=encrypt(landAadharNum))
        return Response({'status': 'Y'})

    else:
        createLog("Verification of tenant failed",
                  initiator=encrypt(landAadharNum))
        return Response({'status': 'N', 'errCode': res['errCode']})


@api_view(['POST'])
def getLandTenants(request):
    data = request.data
    token = data['token']
    land = Landlord.objects.get(token=token)

    t = time.time()

    if land.token == token and land.time - t < 1800:
        tenants = Tenant.objects.filter(landlord=land)
        tenants_ser = serializers.TenantSerializer(tenants, many=True)

        createLog("Tenants of landlord fetched",
                  initiator=encrypt(land.aadharnum))
        return Response({'status': 'Y', 'tenants': tenants_ser.data})

    else:
        createLog("Tenants of landlord failed",
                  initiator=encrypt(land.aadharnum))
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def getLandAddr(request):
    data = request.data
    token = data['token']

    land = Landlord.objects.get(token=token)
    print(land.co)
    t = time.time()

    if land.token == token and land.time - t < 1800:
        def getProperAdd(a):
            spacer = ", "
            if(a == None):
                return ''
            else:
                return str(a)+spacer

        co = land.co
        house = land.house

        addr = getProperAdd(land.street) + getProperAdd(land.lm) + getProperAdd(land.loc) + getProperAdd(land.vtc) + getProperAdd(land.subdist) + \
            getProperAdd(land.dist) + getProperAdd(land.state) + \
            getProperAdd(land.country) + \
            getProperAdd(land.pc) + \
            getProperAdd(land.po)

        createLog("Landlord address fetched",
                  initiator=encrypt(land.aadharnum))
        return Response({'status': 'Y', 'co': co, 'house': house, 'addr': addr})
    else:
        createLog("Landlord address fetch failed",
                  initiator=encrypt(land.aadharnum))
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def uptTenAddr(request):
    data = request.data
    token = data['token']

    ten = Tenant.objects.get(token=token)

    t = time.time()

    if ten.token == token and ten.time - t < 1800:
        co = data['co']
        house = data['house']

        ten.mod_co = co
        ten.mod_house = house

        ten.save()

        # Send updated address to aadhar

        createLog("Tenant address updated", initiator=encrypt(ten.aadharnum))
        return Response({'status': 'Y'})

    else:
        createLog("Tenant address update failed",
                  initiator=encrypt(ten.aadharnum))
        return Response({'status': 'N', 'errCode': 'Invalid Token'})


@api_view(['POST'])
def reduceAddr(request):
    data = request.data
    addr = data["address"]
    new_addr = new_address(addr)
    return Response({'new_addr': new_addr})
