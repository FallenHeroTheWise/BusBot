import requests

import json
from bs4 import BeautifulSoup
from pprint import pprint

def get_api():
    url = 'https://alo141.az/buses/index?language=az'
    try:
        s=requests.Session()
        response = s.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token_value = soup.find('meta', attrs={'name': 'csrf'})
        csrf_token = csrf_token_value.get('content')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    #finding csrf to send
    

    headers = {
    'X-CSRF-Token': csrf_token,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    
    'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,az-AZ;q=0.4,az;q=0.3,tr-TR;q=0.2,tr;q=0.1',
    'Content-Length': '107',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://alo141.az',
    'Referer': 'https://alo141.az/buses/index?language=az',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    response = s.post('https://alo141.az/az/ajax/apiNew1', headers=headers, data={'YII_CSRF_TOKEN': csrf_token})
    return response.text
