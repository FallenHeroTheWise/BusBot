import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import random
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
bot = telepot.Bot('5319724716:AAElD0JgkyeEWdGxW5g0Y0MQdBnlRO7BY_I')
pompa={}
answered=[]
mustcheck=[]
import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from getapi import get_api
def getUpdate():
    
    a=get_api()
    jj=json.loads(a)
    count=0
    buses=[]
    total=0
    for y in jj['BUS']:
        #that's the stupidest way to do it, past me, though I won't fix it
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
    #returning a list of all the buses
    return buses

def sortbynumber(number):
    
    buses=getUpdate()
    
    for b in buses:
        
        if b[0]==number:
            
            return b
        
    #getting a certain bus by its unique id
def updatebynumber(number, buses: list):
    
    for b in buses:

        if b[0]==number:
            
            return b
        
    #getting a certain bus by its unique id with list of buses as an argument 
def sort(number, buses: list):
    
    pprint(len(buses))
    
    crrct=[]
    
    for b in buses:
        
        if b[-1]==number:
            
            crrct.append(b)
            
    #creating a list of matching buses
            
    if number!='85':
        
        routenames=[]
        
        for c in crrct:
        
            if not c[9] in routenames:
                
               routenames.append(c[9])
               
        sorted1=[]
        
        sorted2=[]
        if len(routenames)==2:
            
            for c in crrct:
                
                if c[9]==routenames[0]:
                    
                    sorted1.append(c)
                    
                else:
                    
                    sorted2.append(c)
                    
        elif len(routenames)==1:

            

            for c in crrct:

                if c[9]==routenames[0]:

                    sorted1.append(c)

                    sorted2.append(c)

                else:

                    sorted2.append(c)

                    sorted1.append(c)

            routenames.append(routenames[0])
            
            #getting the routenames to send through telegram
            
        else:
            
            print(number)
            
            raise Exception
        
    if number=='85':
        
        routenames=[]
        
        for c in crrct:
            
            c[9]=c[9].replace('Mərkəzi Bank', '28 Mall')
        
            if not c[9] in routenames:
                
               routenames.append(c[9])
               
        sorted1=[]
        
        sorted2=[]
        
        if len(routenames)==2:
            
            for c in crrct:
                
                c[9]=c[9].replace('Mərkəzi Bank', '28 Mall')
                
                if c[9]==routenames[0]:
                    
                    sorted1.append(c)
                    
                else:
                    
                    sorted2.append(c)
                    
            c[9]=c[9].replace('Mərkəzi Bank', '28 Mall')
            
        elif len(routenames)==1:

            

            for c in crrct:
                
                c[9]=c[9].replace('Mərkəzi Bank', '28 Mall')
                
                if c[9]==routenames[0]:

                    sorted1.append(c)

                    sorted2.append(c)

                else:

                    sorted2.append(c)

                    sorted1.append(c)

            routenames.append(routenames[0])
            
    return [routenames, sorted1, sorted2]

def handle(msg):
    
    pprint(msg)
    
    global pompa
    
    if time.time()-msg['date']>300:
        
    	msg['text']=""
    	
    	print(time.time()-msg['date'])
    	
    text=msg['text']
    
    idd=msg['chat']['id']
    
    if text.startswith('/bus '):
        
        try:
            
            bot.sendMessage(idd, 'Yoxlanılır')
            
            c=sort(text[4:].strip(), buses)
            
            pompa[idd]=c
            
            bot.sendMessage(idd, 'Hansı istiqamət', reply_markup=InlineKeyboardMarkup( inline_keyboard=[ [InlineKeyboardButton(text=c[0][0], callback_data='1'), InlineKeyboardButton(text=c[0][1], callback_data='2')]]))

        except:
            
            bot.sendMessage(idd, 'Yanlış istək')
            
    if text=='/bus':
        
        bot.sendMessage(idd, '/bus avtobus_nomresi')
    
def callbackQuery(query):
    
    global answered
    
    pprint(query)
    
    idd=query['message']['chat']['id']
    
    try:
        
        c=pompa[query['message']['chat']['id']]
        
    except KeyError:
        
        bot.sendMessage(idd, 'Köhnə mesaj')
        
        raise Exception
    
    if query['message']['message_id'] in answered:

        bot.answerCallbackQuery(query['id'], 'Artıq cavablandırılıb')

        raise Exception

    answered.append(query['message']['message_id'])
    
    bot.answerCallbackQuery(query['id'], 'Qəbul edildi')
    
    if query['data'].startswith('c'):
        
        d=updatebynumber(query['data'][1:], buses)
        
        bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'),
                             reply_markup=InlineKeyboardMarkup( inline_keyboard=[[
                                 InlineKeyboardButton(text='Yenilə', callback_data='b'+d[1])]]))
    
        bot.sendMessage(idd, 'Göndərildi')
    if query['data'].startswith('b'):
        
        d=updatebynumber(query['data'][1:], buses)

        mass=bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'), live_period=1200)

        mustcheck.append([mass, time.time(), query['data'][1:]])
    
        bot.sendMessage(idd, 'Göndərildi')
    if query['data']=='1':
        
        for d in c[1]:

            print(d[7], d[8])

            bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'),
                             reply_markup=InlineKeyboardMarkup( inline_keyboard=[[
                                 InlineKeyboardButton(text='Yenilə', callback_data='b'+d[1])]]))
        bot.sendMessage(idd, 'Göndərildi')
    if query['data']=='2':

        for d in c[2]:

            print(d[7], d[8])

            bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'), reply_markup=InlineKeyboardMarkup( inline_keyboard=[[
                                 InlineKeyboardButton(text='Yenilə', callback_data='b'+d[1])]]))

        bot.sendMessage(idd, 'Göndərildi')





def updateEverything(firsttime):

    global buses

    try:

        buses=getUpdate()

        if firsttime==0:

            c=sort('85', buses)
            
            idd=685789544
            
            pompa[idd]=c
                        
            bot.sendMessage(685789544, 'Hansı istiqamət', reply_markup=InlineKeyboardMarkup( inline_keyboard=[ [InlineKeyboardButton(text=c[0][0], callback_data='1'), InlineKeyboardButton(text=c[0][1], callback_data='2')]]))

            firsttime=1
            
    except:
        
        pass
    
    for a in mustcheck:
        
            if time.time()-a[1]>1200:
                
                mustcheck.remove(a)
                
            else:
                
                try:
                    
                    d=updatebynumber(a[2], buses)
                    
                except:
                    
                    mustcheck.remove(a)
                    
                try:
                    
                    bot.editMessageLiveLocation((a[0]['chat']['id'], a[0]['message_id']), d[7].replace(',', '.'), d[8].replace(',', '.'))

                except:
                    
                    print('fail')
    

if __name__ == '__main__':
    
    bot.message_loop({'chat': handle, 'callback_query': callbackQuery})

    firsttime = 0

    updateEverything(firsttime)

    while True:
        
        updateEverything(1)

        time.sleep(7)
    
    
