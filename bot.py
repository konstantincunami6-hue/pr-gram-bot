import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TOKEN') or os.getenv('BOT_TOKEN') or os.getenv('API_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("КРИТИЧЕСКАЯ ОШИБКА: Токен не найден!")
    exit()

bot = telebot.TeleBot(TOKEN)

# Главное меню
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("💰 Заработать"),
        KeyboardButton("📢 Рекламировать")
    )
    keyboard.add(
        KeyboardButton("🧾 Чеки"),
        KeyboardButton("📊 Мой кабинет")
    )
    keyboard.add(
        KeyboardButton("🔊 ОП (Проверка подписки)"),
        KeyboardButton("🤖 Наши боты / Статистика")
    )
    keyboard.add(
        KeyboardButton("🔗 Полезные ссылки"),
        KeyboardButton("📝 Инструкция")
    )
    return keyboard

# Подменю "Мой кабинет"
def get_cabinet_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("💰 Пополнить баланс"),
        KeyboardButton("👥 Реферальная система")
    )
    keyboard.add(
        KeyboardButton("📈 Уровневая система"),
        KeyboardButton("🎒 Мои задания")
    )
    keyboard.add(
        KeyboardButton("🌐 Изменить язык"),
        KeyboardButton("❌ Отключить уведомления")
    )
    keyboard.add(KeyboardButton("🔙 Назад в меню"))
    return keyboard

# Подменю "Пополнить баланс"
def get_topup_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(
        KeyboardButton("90,000 belcoin = 50 ⭐"),
        KeyboardButton("180,000 belcoin = 100 ⭐"),
        KeyboardButton("450,000 belcoin = 250 ⭐"),
        KeyboardButton("1,350,000 belcoin = 750 ⭐"),
        KeyboardButton("2,700,000 belcoin = 1499 ⭐"),
        KeyboardButton("4,500,000 belcoin = 2499 ⭐")
    )
    keyboard.add(KeyboardButton("⭐ Другая сумма"))
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
👋 Приветствуем вас в PR GRAM!

📌 Обязательная проверка подписки в ваших чатах.
PR GRAM обеспечивает удобные и гибкие настройки для проверки подписок с широким выбором фильтров.

📖 Ознакомьтесь с инструкцией для ОП

📈 Рекламная система PR GRAM для роста живой аудитории позволяет эффективно продвигать:
• 👥 Подписки на каналы и группы
• 👁 Просмотры контента
• ⚡️ Премиум-бусты
• 🤖 Продвижение ботов

📘 Инструкция по продвижению

💡 Используя бота, вы автоматически соглашаетесь с нашей политикой конфиденциальности.
    """.strip()

    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text

    if text == "📊 Мой кабинет":
        cabinet_text = f"""
Ваш кабинет:

🔑 Мой ID: {message.from_user.id}
💰 Баланс: 0 belcoin
        """.strip()

        bot.send_message(message.chat.id, cabinet_text, reply_markup=get_cabinet_keyboard())

    elif text == "💰 Пополнить баланс":
        topup_text = """
Если возникли проблемы с пополнением — обращайтесь: @Tsunami_TG

Введите сумму пополнения в belcoin
или выберите:
        """.strip()

        bot.send_message(message.chat.id, topup_text, reply_markup=get_topup_keyboard())

    elif text == "🔙 Назад" or text == "🔙 Назад в меню":
        bot.send_message(message.chat.id, "Вы вернулись в предыдущее меню 👇", reply_markup=get_cabinet_keyboard())

    elif text in ["💰 Заработать", "📢 Рекламировать", "🧾 Чеки", "👥 Реферальная система", "📈 Уровневая система", "🎒 Мои задания", "🌐 Изменить язык", "❌ Отключить уведомления", "🔊 ОП (Проверка подписки)", "🤖 Наши боты / Статистика", "🔗 Полезные ссылки", "📝 Инструкция"]:
        bot.send_message(message.chat.id, "Эта функция в разработке 🚧", reply_markup=get_main_keyboard() if text in ["💰 Заработать", "📢 Рекламировать", "🧾 Чеки", "🔊 ОП (Проверка подписки)", "🤖 Наши боты / Статистика", "🔗 Полезные ссылки", "📝 Инструкция"] else get_cabinet_keyboard())

    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню 👇", reply_markup=get_main_keyboard())

print("Бот PR GRAM с пополнением belcoin успешно запущен!")
bot.infinity_polling()
