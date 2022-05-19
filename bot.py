import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import bus
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
bot = telepot.Bot('5319724716:AAElD0JgkyeEWdGxW5g0Y0MQdBnlRO7BY_I')
pompa={}
answered=[]
mustcheck=[]
def sortbynumber(number):
    buses=bus.getUpdate()
    for b in buses:
        if b[0]==number:
            return b
def updatebynumber(number, buses):
    
    for b in buses:
        if b[0]==number:
            return b
def sort(number, buses):
    
    pprint(len(buses))
    crrct=[]
    for b in buses:
        if b[-1]==number:
            crrct.append(b)
    
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
        mass=bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'), live_period=360)
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
bot.message_loop({'chat': handle, 'callback_query': callbackQuery})
while True:
    buses=bus.getUpdate()
    
    for a in mustcheck:
            if time.time()-a[1]>360:
                break
            else:
                d=updatebynumber(a[2], buses)
                try:
                    bot.editMessageLiveLocation((a[0]['chat']['id'], a[0]['message_id']), d[7].replace(',', '.'), d[8].replace(',', '.'))
                except:
                    pass
    time.sleep(2)


