import requests
from telebot import TeleBot

TG_TOKEN = 'тут был токен'
bot = TeleBot(TG_TOKEN)
VK_TOKEN = 'и ещё один'

VK_API_URL = 'https://api.vk.com/method/'
VK_API_VERSION = '5.131'


def SetStatus(message):
    response = requests.post(
        f'{VK_API_URL}status.set',
        params={
            'access_token': VK_TOKEN,
            'text': message,
            'v': VK_API_VERSION
        },
        verify=False
    )
    return response.json()


@bot.message_handler(content_types=['text'])
def Exec(message):
    result = SetStatus(message.text)
    if 'response' in result:
        bot.send_message(message.chat.id, f"Обновил профиль с новым текстом: \"{message.text}\"")
    else:
        bot.send_message(message.chat.id, f"щаща, щаща")
        print(result)


bot.polling(none_stop=True)
