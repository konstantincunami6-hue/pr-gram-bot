import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8507575219:AAEyv1TiJJbXeDQDHSMs2E-QoRvyuyFrZTw'  # ← твой токен

bot = telebot.TeleBot(TOKEN)

# Главное меню с кнопкой ОП
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton("🔊 ОП (Проверка подписки)"))
    return keyboard

# Клавиатура под сообщением ОП
def get_op_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("Добавить бота в чат"))
    keyboard.add(KeyboardButton("Добавить бота в канал"))
    keyboard.add(KeyboardButton("Чат поддержки"))
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "Привет! Это тестовая версия. Нажми кнопку ОП."
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text

    if text == "🔊 ОП (Проверка подписки)":
        op_text = """
✅ *Функция проверки подписки на канал/чат*

▸ *Шаг 1.* Добавьте бота в ваш чат с правами администратора.  
   (Можно с помощью этой ссылки: t.me/TSUGRAM_PRBOT?startgroup=true)

▸ *Шаг 2.* Добавьте бота в администраторы канала/чата.

*Шаг 3.* В чате напишите команду:  
`/setup @канал`

Если ты видишь этот текст — кнопка работает!  
Напиши "работает", если всё ок.
        """.strip()

        bot.send_message(message.chat.id, op_text, parse_mode='Markdown', reply_markup=get_op_keyboard())

    elif text == "🔙 Назад":
        bot.send_message(message.chat.id, "Вернулись в главное меню", reply_markup=get_main_keyboard())

    else:
        bot.send_message(message.chat.id, "Нажми на кнопку ОП", reply_markup=get_main_keyboard())

print("Тестовый бот запущен — кнопка ОП должна работать!")
bot.infinity_polling()
