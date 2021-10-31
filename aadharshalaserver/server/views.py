from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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


@api_view(['GET'])
def get_address(request):
    reqData = request.data
    aadharnum = reqData['aadharnum']
    landlord = Landlord.objects.get(aadharnum=aadharnum)
    tenants = Tenant.objects.filter(landlord=landlord)
    tenants_ser = serializers.TenantSerializer(tenants, many=True)
    return Response({"tenants": tenants_ser.data})


def get_app_address(request):
    reqData = request.data
    aadharnum = reqData['aadharnum']
    landlord = Landlord.objects.get(aadharnum=aadharnum)

    landlord_ser = serializers.LandlordSerializer(landlord)
    return Response({"lanlord": landlord_ser.data})


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

    if(res['status'] == 'Y'):
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

    if(res['status'] == 'y'):
        land = Landlord.objects.get_or_create(aadharnum=aadharnum)
        ten = Tenant.objects.get_or_create(aadharnum=aadharnum)

        land.token = token
        ten.token = token

        t = time.time()

        land.time = t
        ten.time = t

        land.save()
        ten.save()

        return Response({'status': 'Y', token: token})

    return Response({'status': 'N', 'errCode': res['errCode']})
