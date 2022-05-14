import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
def getUpdate():
    r=requests.get('https://alo141.az/az/ajax/apiNew1')
    a=r.text[6:-1].split(':')
    jj=json.loads(r.text)
    pprint(jj['BUS'][0])
    
    
    b=r.text[6:-1].split('"')
    count=0
    buses=[]
    total=0
    for y in jj['BUS']:
        if True:
            x=y['@attributes']
            busid=x['BUS_ID']
        
            plate=x['PLATE']
        
            d=x['DRIVER_NAME']
    
            prevstop=x['PREV_STOP']
        
            current=x['CURRENT_STOP']
        
            speed=x['SPEED']

            model=x['BUS_MODEL']

            lat=x['LATITUDE']
    
            lon=x['LONGITUDE']
        
            
            name=x['ROUTE_NAME']
            code=x['DISPLAY_ROUTE_CODE']
            buses.append([busid, plate, d, prevstop, current, speed, model, lat, lon, name, code])
            
            
                
                     
    
    
    
        
        
    return buses

