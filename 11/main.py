# -*- coding: utf-8 -*-
from handlers import *


messagesHandlersMap = {
    States.start: handleStart,
    States.selectCur: handleCurrency,
    States.dateFrom: handleDateFrom,
    States.dateEnd: handleDateTo,
    None: defaultMessage,
}

@bot.message_handler(commands=['start'])
def start(message):
    handleStart(message)


@bot.message_handler(content_types=['text'])
def handleMessage(message):
    if message.from_user.id in userStateMap:
        runfunc = messagesHandlersMap[userStateMap[message.from_user.id]]
    else:
        runfunc = messagesHandlersMap[None]

    runfunc(message)

bot.polling(none_stop=True)
