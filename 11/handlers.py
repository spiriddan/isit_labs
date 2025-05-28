from telebot import types
import datetime
import xml.dom.minidom
import requests
import matplotlib.pyplot as plt
import os

from maps import *

# id -> state
userStateMap = {}

# id -> UserData
userDataMap = {}


def handleCurrency(message):
    cur = message.text
    if not (cur in currencies):
        bot.send_message(message.chat.id, '❌ Выберите вариант из меню или нажмите /start')
        return

    userStateMap[message.from_user.id] = States.dateFrom
    userDataMap[message.from_user.id] = UserData(currenciesMap[message.text])
    bot.send_message(message.chat.id, 'Отправьте дату начала промежутка в формате dd/mm/yyyy')


def handleDateFrom(message):
    dateFrom = message.text
    if not isDatetimeCorrect(dateFrom):
        bot.send_message(message.chat.id, '❌ Отправьте дату в формате dd/mm/yyyy или нажмите /start')
        return

    userStateMap[message.from_user.id] = States.dateEnd
    userDataMap[message.from_user.id].dateFrom = dateFrom
    bot.send_message(message.chat.id, 'Отправьте дату окончания промежутка в формате dd/mm/yyyy')


def handleDateTo(message):
    dateTo = message.text
    if not isDatetimeCorrect(dateTo):
        bot.send_message(message.chat.id, '❌ Отправьте дату в формате dd/mm/yyyy или нажмите /start')
        return

    userStateMap[message.from_user.id] = States.dateEnd
    userDataMap[message.from_user.id].dateEnd = dateTo

    searchCurrency(message, userDataMap[message.from_user.id])


def handleStart(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cur in currencies:
        keyboard.add(cur)
    userStateMap[message.from_user.id] = States.selectCur
    bot.send_message(message.chat.id, "Привет, выбери валюту", reply_markup=keyboard)


def defaultMessage(message):
    bot.send_message(message.chat.id, '❌ Что-то не так, нажмите /start')


def isDatetimeCorrect(timeStr: str) -> bool:
    try:
        datetime.datetime.strptime(timeStr, "%d/%m/%Y")
    except:
        return False

    return True


def searchCurrency(message, userData: UserData):
    dateFrom, dateEnd, currency = userData.dateFrom, userData.dateEnd, userData.currency

    req = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={dateFrom}&date_req2={dateEnd}&VAL_NM_RQ={currency['id']}"
    resp = requests.get(req)
    print(req)

    parsed = xml.dom.minidom.parseString(resp.text)
    parsed.normalize()
    days = [[i.getAttribute("Date"), i.childNodes[1].childNodes[0].nodeValue] for i in parsed.getElementsByTagName("Record")]

    userStateMap[message.from_user.id] = States.start
    userDataMap[message.from_user.id] = None

    x = [i[0][:5] for i in days]
    y = [float(i[1].replace(',', '.')) for i in days]
    filename = "plot.png"

    plt.plot(x, y, marker="o")
    plt.xticks(rotation=35)
    plt.title(f"Курсы (к рублю) валюты с кодом {currency['flag']}{currency['id']}")

    plt.savefig(filename)
    plt.close()

    with open(filename, "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Вот запрашиваемые курсы")

    os.remove(filename)

