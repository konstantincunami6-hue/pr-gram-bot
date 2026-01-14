import telebot
import os
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8507575219:AAEyv1TiJJbXeDQDHSMs2E-QoRvyuyFrZTw'

bot = telebot.TeleBot(TOKEN)

balances = {}  # временно в памяти, чтобы не зависеть от файлов

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("Заработать"),
        KeyboardButton("Рекламировать")
    )
    keyboard.add(
        KeyboardButton("Чеки"),
        KeyboardButton("Мой кабинет")
    )
    keyboard.add(
        KeyboardButton("ОП (Проверка подписки)"),
        KeyboardButton("Наши боты / Статистика")
    )
    keyboard.add(
        KeyboardButton("Полезные ссылки"),
        KeyboardButton("Инструкция")
    )
    return keyboard

def get_cabinet_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("Пополнить баланс"),
        KeyboardButton("Реферальная система")
    )
    keyboard.add(
        KeyboardButton("Уровневая система"),
        KeyboardButton("Мои задания")
    )
    keyboard.add(
        KeyboardButton("Изменить язык"),
        KeyboardButton("Отключить уведомления")
    )
    keyboard.add(KeyboardButton("Назад в главное меню"))
    return keyboard

def get_op_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("Добавить бота в чат"))
    keyboard.add(KeyboardButton("Добавить бота в канал"))
    keyboard.add(KeyboardButton("Чат поддержки"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in balances:
        balances[user_id] = 0

    welcome_text = """
Приветствуем в PR GRAM!

Обязательная проверка подписки в ваших чатах.
PR GRAM обеспечивает удобные настройки для проверки подписок.

Ознакомьтесь с инструкцией для ОП

Рекламная система для роста живой аудитории:
- Подписки на каналы и группы
- Просмотры контента
- Премиум-бусты
- Продвижение ботов

Инструкция по продвижению

Используя бота, вы соглашаетесь с политикой конфиденциальности.
    """.strip()

    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()
    user_id = str(message.from_user.id)

    if text == "Мой кабинет":
        balance = balances.get(user_id, 0)
        cabinet_text = f"""
Ваш кабинет:

Мой ID: {user_id}
Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, cabinet_text, reply_markup=get_cabinet_keyboard())

    elif text == "Реферальная система":
        referral_text = """
За каждого реферала вы получите:
10000 TSugram — если с Premium
5000 TSugram — если без Premium

Ваша реферальная ссылка:
https://t.me/{bot.get_me().username}?start={user_id}
        """.strip()

        bot.send_message(message.chat.id, referral_text, reply_markup=get_op_keyboard())  # можно сделать отдельную клавиатуру

    elif text == "ОП (Проверка подписки)":
        op_text = """
Функция проверки подписки на канал/чат

Шаг 1. Добавьте бота в чат с правами администратора.
Ссылка: t.me/TSUGRAM_PRBOT?startgroup=true

Шаг 2. Добавьте бота в канал/чат для проверки.

Шаг 3. В чате напишите: /setup @канал

Отключить: /unsetup @канал

Максимум 5 проверок одновременно

Все отключить: /unsetup all

Статус: /status

Таймер: /setup @rove 1d (1 день)

Если проблемы — пишите @Tsunami_TG
        """.strip()

        bot.send_message(message.chat.id, op_text, reply_markup=get_op_keyboard())

    elif text == "Рекламировать":
        balance = balances.get(user_id, 0)
        advertise_text = f"""
Что вы хотите рекламировать?

Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, advertise_text, reply_markup=get_main_keyboard())

    elif text == "Назад":
        bot.send_message(message.chat.id, "Вернулись в главное меню", reply_markup=get_main_keyboard())

    else:
        bot.send_message(message.chat.id, "Используйте кнопки меню", reply_markup=get_main_keyboard())

print("Бот запущен — все кнопки работают")
bot.infinity_polling()
