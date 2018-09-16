import requests
import json

def get_access_token():
    api_url = 'https://authservice.priaid.ch/login'
    api_key = 'w5BLe_GMAIL_COM_AUT'
    hashed_credentials = 'PL/aRUUf9uFCl4Bt+cQApw=='
    headers = {'Authorization': 'Bearer ' + api_key + ':' + hashed_credentials}
    response = requests.post(api_url, headers=headers).json()
    access_token = response["Token"]
    return access_token