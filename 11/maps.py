import telebot
from enum import Enum


TOKEN = 'и даже тут был токен'
bot = telebot.TeleBot(TOKEN)


# <Item ID="R01010">
#     <Name>Австралийский доллар</Name>
#     <EngName>Australian Dollar</EngName>
#     <Nominal>1</Nominal>
#     <ParentCode>R01010 </ParentCode>
# </Item>
# <Item ID="R01535">
#     <Name>Норвежская крона</Name>
#     <EngName>Norwegian Krone</EngName>
#     <Nominal>10</Nominal>
#     <ParentCode>R01535 </ParentCode>
# </Item>


currencies = ["🇦🇺 AUD", "🇳🇴 NOK"]

currenciesMap = {
    currencies[0]: {
        "id": "R01010",
        "flag": "🇦🇺"
    },
    currencies[1]: {
        "id": "R01535",
        "flag": "🇳🇴"
    }
}


class States(Enum):
    start = 0
    selectCur = 1
    dateFrom = 2
    dateEnd = 3


class UserData:
    def __init__(self, cur):
        self.currency = cur
        self.dateFrom = ""
        self.dateEnd = ""
