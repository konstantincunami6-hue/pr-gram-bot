import telebot
import os
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TOKEN') or '8507575219:AAEyv1TiJJbXeDQDHSMs2E-QoRvyuyFrZTw'  # ← твой токен

bot = telebot.TeleBot(TOKEN)

# Файл для баланса пользователей
BALANCE_FILE = 'balances.json'

def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_balances(balances):
    with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(balances, f, ensure_ascii=False, indent=2)

balances = load_balances()

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
    keyboard.add(KeyboardButton("🔙 Назад в главное меню"))
    return keyboard

# Подменю "Рекламировать"
def get_advertise_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton("Канал"),
        KeyboardButton("Группу")
    )
    keyboard.add(
        KeyboardButton("Пост"),
        KeyboardButton("Бот")
    )
    keyboard.add(
        KeyboardButton("Премиум буст (заряды)"),
        KeyboardButton("Реакции")
    )
    keyboard.add(KeyboardButton("Настройка авто-заданий"))
    keyboard.add(KeyboardButton("Мои задания"))
    keyboard.add(KeyboardButton("← Назад"))
    return keyboard

# Подменю "Тип подписок" для канала
def get_subscription_type_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("1. Доступно для всех пользователей"))
    keyboard.add(KeyboardButton("2. Только для пользователей с Telegram Premium"))
    keyboard.add(KeyboardButton("← Назад"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in balances:
        balances[user_id] = 0
        save_balances(balances)

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
    user_id = str(message.from_user.id)

    if text == "📢 Рекламировать":
        balances = load_balances()
        balance = balances.get(user_id, 0)
        advertise_text = f"""
Что вы хотите рекламировать?

💰 Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, advertise_text, reply_markup=get_advertise_keyboard())

    elif text == "Канал":
        balances = load_balances()
        balance = balances.get(user_id, 0)
        subscription_text = f"""
Выберите тип подписок:

1. Доступно для всех пользователей — доступно всем пользователям PR GRAM,  
   быстрое привлечение PR GRAM,  
   широкой аудитории.  
   🔴 Минимальная цена за ед. — 600 TSugram

2. Только для пользователей с Telegram Premium ⭐ —  
   доступно только пользователям с Telegram Premium,  
   что гарантирует более качественную аудиторию.  
   🔴 Минимальная цена за ед. — 1 400 TSugram
        """.strip()

        bot.send_message(message.chat.id, subscription_text, reply_markup=get_subscription_type_keyboard())

    elif text == "← Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню 👇", reply_markup=get_main_keyboard())

    elif text == "📊 Мой кабинет":
        balances = load_balances()
        balance = balances.get(user_id, 0)
        cabinet_text = f"""
Ваш кабинет:

🔑 Мой ID: {user_id}
💰 Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, cabinet_text, reply_markup=get_cabinet_keyboard())

    # Добавь сюда остальные обработчики (Реферальная система, Мои задания и т.д.)

    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню 👇", reply_markup=get_main_keyboard())

print("Бот запущен — кнопка 'Рекламировать' → 'Канал' с типами подписок работает!")
bot.infinity_polling()
   
