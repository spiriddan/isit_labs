# -*- coding: utf-8 -*-
import telebot
from telebot import types

TOKEN = 'тут был токен'
bot = telebot.TeleBot(TOKEN)

# Счётчики нажатий
click_counter = {}

# оценки
likes = 0
dislikes = 0

# Увеличиваем счётчик
def increment_click(key):
    click_counter[key] = click_counter.get(key, 0) + 1


# Главное меню
@bot.message_handler(commands=['start'])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🍕 Еда', '🎮 РаЗвЛеЧеНиЯ', '📚 Обучение', 'Оценочку 👍')
    bot.send_message(m.chat.id, "Привет! Что тебя интересует?", reply_markup=keyboard)


# Обработка кнопок
@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    increment_click(text)

    if text == '🍕 Еда':
        food_menu(message)
    elif text == '🎮 РаЗвЛеЧеНиЯ':
        fun_menu(message)
    elif text == '📚 Обучение':
        study_menu(message)
    elif text == 'Пицца 🍕':
        bot.send_message(message.chat.id, f'Вы выбрали Пиццу! 🍕 (нажато {click_counter[text]} раз)')
    elif text == 'Бургер 🍔':
        bot.send_message(message.chat.id, f'Вы выбрали Бургер! 🍔 (нажато {click_counter[text]} раз)')
    elif text == 'Фрукты 🍉':
        bot.send_message(message.chat.id, f'Вы выбрали Фрукты! 🍉 (нажато {click_counter[text]} раз)')
    elif text == 'Игры 🎲':
        bot.send_message(message.chat.id, f'Вы выбрали Игры! 🎲 (нажато {click_counter[text]} раз)')
    elif text == '😂 Мемы 😂':
        bot.send_message(message.chat.id, f'Вы выбрали Мемы! 😂 (нажато {click_counter[text]} раз)')
    elif text == 'Фильмы 🎬':
        bot.send_message(message.chat.id, f'Вы выбрали Фильмы! 🎬 (нажато {click_counter[text]} раз)')
    elif text == 'ИСИТ 💻':
        bot.send_message(message.chat.id, f'Вы выбрали ИСИТ! 💻 (нажато {click_counter[text]} раз)')
    elif text == 'История 🌍':
        bot.send_message(message.chat.id, f'Вы выбрали Историю! 🌍 (нажато {click_counter[text]} раз)')
    elif text == 'Оценочку 👍':
        likes_menu(message)
    elif text == 'Назад 🔙':
        start(message)
    else:
        bot.send_message(message.chat.id, 'Выберите вариант из меню или нажмите /start')


def food_menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Пицца 🍕', 'Бургер 🍔', 'Фрукты 🍉', 'Назад 🔙')
    bot.send_message(message.chat.id, "Чем хочешь перекусить?", reply_markup=kb)


def fun_menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Игры 🎲', '😂 Мемы 😂', 'Фильмы 🎬', 'Назад 🔙')
    bot.send_message(message.chat.id, "Как развлекаться будешь?", reply_markup=kb)


def study_menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('ИСИТ 💻', 'История 🌍', 'Назад 🔙')
    bot.send_message(message.chat.id, "Чему хочешь научиться?", reply_markup=kb)


def likes_menu(message):
    global likes, dislikes
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f'👍 Мне нравится ({likes} оценили)', callback_data='like'),
        types.InlineKeyboardButton(f'👎 Мне не нравится ({dislikes} не оценили)', callback_data='dislike')
    )
    bot.send_message(message.chat.id, "Оцените этот бот:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['like', 'dislike'])
def callback_handler(call):
    global likes, dislikes
    respText = ""
    if call.data == 'like':
        likes += 1
        respText = "спасибо за лайк))"
    elif call.data == 'dislike':
        dislikes += 1
        respText = "ну и не надо, не пиши сюда больше"

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f'👍 Мне нравится ({likes} оценили)', callback_data='like'),
        types.InlineKeyboardButton(f'👎 Мне не нравится ({dislikes} не оценили)', callback_data='dislike')
    )

    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup)

    bot.answer_callback_query(call.id, respText)


bot.polling(none_stop=True)
