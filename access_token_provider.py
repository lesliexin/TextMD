import requests
import json

def get_access_token():
    api_url = 'https://authservice.priaid.ch/login'
    api_key = 'm4BRe_HOTMAIL_COM_AUT'
    hashed_credentials = '2+npCDnxnvv8Lt8VKo35mg=='
    headers = {'Authorization': 'Bearer ' + api_key + ':' + hashed_credentials}
    response = requests.post(api_url, headers=headers).json()
    access_token = response["Token"]
    return access_token