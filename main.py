import json
import time
from pprint import pprint
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from getapi import get_api
from dataclasses import dataclass

bot = telepot.Bot('<API_KEY>')
message_ids = {}
answered = []
must_check = []


class Buses:
    def __init__(self, content=None):
        if content is None:
            content = []
        self.content = content

    def __add__(self, other):
        iter(other)
        # check if object is iterable or not if not it will raise a TypeError
        return self.content + other

    def __iadd__(self, other):
        if type(other) == Bus:
            self.content.append(other)
            return self
        else:
            iter(other)
            # check if object is iterable or not if not it will raise a TypeError
            self.content.extend(other)
            return self

    def __iter__(self):
        return BusesIterator(self)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item):
        return self.content[item]


class BusesIterator:
    def __init__(self, bus_list):
        self._bus_list = bus_list
        self._index = 0

    def __next__(self):
        if self._index < len(self._bus_list.content):
            self._index += 1
            return self._bus_list.content[self._index - 1]
        raise StopIteration


@dataclass()
class Bus:
    bus_id: str
    plate: str
    driver_name: str
    previous_stop: str
    current_stop: str
    speed: int
    model: int
    lat: int
    lon: int
    name: str
    bus_code: str

    def __iter__(self):
        BusIterator(self)

    def __getitem__(self, item):
        return list(self.__dict__.values())[item]

    def __setitem__(self, key, value):
        self.__dict__.update({f'{list(self.__dict__.items())[key][0]}': value})


class BusIterator:
    def __init__(self, other):
        self._index = 0
        self._list = list(other.__dict__.keys())

    def __next__(self):
        if self._index < len(self._list):
            self._index += 1
            return self._list[self._index - 1]


def get_update():
    a = get_api()
    json_grabbed = json.loads(a)
    buses1 = Buses([])
    for y in json_grabbed['BUS']:

        x = y['@attributes']


        buses1 += Bus(bus_id=x['BUS_ID'], plate=x["PLATE"], driver_name=x["DRIVER_NAME"], previous_stop=x['PREV_STOP'],
                      current_stop=x["CURRENT_STOP"], speed=x['SPEED'], model=x['BUS_MODEL'], lat=x['LATITUDE'],
                      lon=x['LONGITUDE'], name=x['ROUTE_NAME'], bus_code=x['DISPLAY_ROUTE_CODE'])
    # returning a iterable and subscriptable object of all the buses
    return buses1


def updatebynumber(number, buses: Buses):
    for b in buses:

        if b[0] == number:
            return b

    # getting a certain bus by its unique id with list of buses as an argument


def sort(number, buses: Buses):
    pprint(len(buses))

    crrct = []

    for b in buses:

        if b[-1] == number:
            crrct.append(b)

    # creating a list of matching buses

    if number != '85':

        routenames = []

        for c in crrct:

            if not c[9] in routenames:
                routenames.append(c[9])

        sorted1 = []

        sorted2 = []
        if len(routenames) == 2:

            for c in crrct:

                if c[9] == routenames[0]:

                    sorted1.append(c)

                else:

                    sorted2.append(c)

        elif len(routenames) == 1:

            for c in crrct:

                if c[9] == routenames[0]:

                    sorted1.append(c)

                    sorted2.append(c)

                else:

                    sorted2.append(c)

                    sorted1.append(c)

            routenames.append(routenames[0])

            # getting the routenames to send through telegram

        else:

            print(number)

            raise Exception

    if number == '85':

        routenames = []

        for c in crrct:

            c[9] = c[9].replace('Mərkəzi Bank', '28 Mall')

            if not c[9] in routenames:
                routenames.append(c[9])

        sorted1 = []

        sorted2 = []

        if len(routenames) == 2:

            for c in crrct:

                c[9] = c[9].replace('Mərkəzi Bank', '28 Mall')

                if c[9] == routenames[0]:

                    sorted1.append(c)

                else:

                    sorted2.append(c)

            c[9] = c[9].replace('Mərkəzi Bank', '28 Mall')

        elif len(routenames) == 1:

            for c in crrct:

                c[9] = c[9].replace('Mərkəzi Bank', '28 Mall')

                if c[9] == routenames[0]:

                    sorted1.append(c)

                    sorted2.append(c)

                else:

                    sorted2.append(c)

                    sorted1.append(c)

            routenames.append(routenames[0])

    return [routenames, sorted1, sorted2]


def handle(msg):
    pprint(msg)

    global message_ids

    if time.time() - msg['date'] > 300:
        msg['text'] = ""

        print(time.time() - msg['date'])

    text = msg['text']

    idd = msg['chat']['id']

    if text.startswith('/bus '):

        try:

            bot.sendMessage(idd, 'Yoxlanılır')

            c = sort(text[4:].strip(), buses1)

            message_ids[idd] = c

            bot.sendMessage(idd, 'Hansı istiqamət', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=c[0][0], callback_data='1'),
                 InlineKeyboardButton(text=c[0][1], callback_data='2')]]))

        except:

            bot.sendMessage(idd, 'Yanlış istək')

    if text == '/bus':
        bot.sendMessage(idd, '/bus avtobus_nomresi')


def callback_query(query):
    global answered

    pprint(query)

    idd = query['message']['chat']['id']

    try:

        c = message_ids[query['message']['chat']['id']]

    except KeyError:

        bot.sendMessage(idd, 'Köhnə mesaj')

        raise Exception

    if query['message']['message_id'] in answered:
        bot.answerCallbackQuery(query['id'], 'Artıq cavablandırılıb')

        raise Exception

    answered.append(query['message']['message_id'])

    bot.answerCallbackQuery(query['id'], 'Qəbul edildi')

    if query['data'].startswith('c'):
        d = updatebynumber(query['data'][1:], buses1)

        bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'),
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                             InlineKeyboardButton(text='Yenilə', callback_data='b' + d[1])]]))

        bot.sendMessage(idd, 'Göndərildi')
    if query['data'].startswith('b'):
        d = updatebynumber(query['data'][1:], buses1)

        mass = bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'), live_period=1200)

        must_check.append([mass, time.time(), query['data'][1:]])

        bot.sendMessage(idd, 'Göndərildi')
    if query['data'] == '1':

        for d in c[1]:
            print(d[7], d[8])

            bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                 InlineKeyboardButton(text='Yenilə', callback_data='b' + d[1])]]))
        bot.sendMessage(idd, 'Göndərildi')
    if query['data'] == '2':

        for d in c[2]:
            print(d[7], d[8])

            bot.sendLocation(idd, d[7].replace(',', '.'), d[8].replace(',', '.'),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                 InlineKeyboardButton(text='Yenilə', callback_data='b' + d[1])]]))

        bot.sendMessage(idd, 'Göndərildi')


def update_everything(first_time):
    global buses1

    try:

        buses1 = get_update()

        if first_time:
            c = sort('85', buses1)

            idd = 685789544

            message_ids[idd] = c

            bot.sendMessage(685789544, 'Hansı istiqamət', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=c[0][0], callback_data='1'),
                 InlineKeyboardButton(text=c[0][1], callback_data='2')]]))

        pass
    except:
        pass

    for a in must_check:

        if time.time() - a[1] > 1200:

            must_check.remove(a)

        else:

            try:

                d = updatebynumber(a[2], buses1)

            except:

                must_check.remove(a)

            try:

                bot.editMessageLiveLocation((a[0]['chat']['id'], a[0]['message_id']), d[7].replace(',', '.'),
                                            d[8].replace(',', '.'))

            except:

                print('fail')


if __name__ == '__main__':

    bot.message_loop({'chat': handle, 'callback_query': callback_query})

    first_time = 1

    update_everything(first_time)

    while True:
        update_everything(0)

        time.sleep(7)
