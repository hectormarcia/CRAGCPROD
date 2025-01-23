import requests
from django.http import JsonResponse
from django.conf import settings

dev_risk_assess_url='https://glencore-dev.risk.coupahost.com/api'


def coupa_oauth():
    url = settings.OAUTH_PATH # 'https://s2pconsulting-coupalink-new-demo.coupacloud.com/oauth2/token'
    clientid = settings.OAUTH_CLIENT_ID # '3d1d73f631cf565c49472f59ad15b128'
    clientsecret = settings.OAUTH_CLIENT_SECRET # 'eee386f0af43ff44a7e0ef142b8ee42d92f646b28b634c47af1be49ec003f8f8'
    scope = settings.OAUTH_SCOPE # 'core.supplier.read core.supplier.write core.contract.write core.contract.read'
    payload = 'grant_type=client_credentials&client_id={0}&client_secret={1}&scope={2}'.format(clientid, clientsecret, scope)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    return data

def getcrasupplierfields(token, guid):
    fields = None
    url = settings.COUPA_CRA_API_PATH + '/suppliers/{0}/extensionfields?limit=200'.format(guid)
    print('url: ' + url)
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print('getcrasupplierfields')
    # print(response)
    data = response.json()
    print(data)
    fields = data['result']['extensionFields'] # just blank if supplier has none
    return fields

def getcrasupplierguidbyname(token, suppliername):
    guid = None
    url = settings.COUPA_CRA_API_PATH + '/suppliers?name[eq]={0}'.format(suppliername)
    print('url: ' + url)
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    guid = data['result']['suppliers'][0]['entityId']
    print(guid)
    return guid

# but we are filtering to only get the name
def getcoresupplierdetails(token, supplierid):
    url = settings.COUPA_API_PATH + "/suppliers/{0}?fields=[\"id\",\"name\",\"number\",{{\"supplier_risk_detail\": [\"id\",{{\"custom_fields\":[]}}]}}]".format(supplierid)
    print('url: ' + url)
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    return data
        