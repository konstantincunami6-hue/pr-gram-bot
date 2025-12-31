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

# Клавиатура для реферальной системы
def get_referral_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("📤 Поделиться ссылкой"))
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
    user_id = message.from_user.id

    if text == "📊 Мой кабинет":
        cabinet_text = f"""
Ваш кабинет:

🔑 Мой ID: {user_id}
💰 Баланс: 0 TSugram
        """.strip()

        bot.send_message(message.chat.id, cabinet_text, reply_markup=get_cabinet_keyboard())

    elif text == "👥 Реферальная система":
        referral_text = f"""
За каждого, кто перейдёт по вашей ссылке, вы получите:
⭐ 10 000 TSugram — если реферал с Telegram Premium
⭐ 5 000 TSugram — если без Telegram Premium
⭐ 3 000 TSugram — если реферал присоединился через функцию ОП

Ваш уровень: ⭐ Мастер заданий

А также постоянный доход от их активности:
🔥 + 10% - от суммы пополнения
🔥 + 5% - от выполнения заданий

⬆ Повышайте ваш уровень для увеличения вознаграждения от активности рефералов. → подробнее в Уровневой системе

📊 Статистика за весь период:
👥 Вы пригласили: 0
💰 Ваш заработок от рефералов:
• от пополнений рефералами 0 TSugram
• от выполнения заданий рефералами 0 TSugram

🔗 Ваша реферальная ссылка:
https://t.me/{bot.get_me().username}?start={user_id}
        """.strip()

        bot.send_message(message.chat.id, referral_text, reply_markup=get_referral_keyboard())

    elif text == "📤 Поделиться ссылкой":
        share_text = f"Присоединяйся в PR GRAM и зарабатывай TSugram!\nМоя реферальная ссылка:\nhttps://t.me/{bot.get_me().username}?start={user_id}"
        bot.send_message(message.chat.id, share_text, reply_markup=get_referral_keyboard())

    elif text == "🔙 Назад":
        bot.send_message(message.chat.id, "Вы вернулись в кабинет 👇", reply_markup=get_cabinet_keyboard())

    elif text == "🔙 Назад в меню":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню 👇", reply_markup=get_main_keyboard())

    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню 👇", reply_markup=get_main_keyboard())

print("Бот PR GRAM с реферальной системой и кнопкой 'Поделиться ссылкой' успешно запущен!")
bot.infinity_polling()   
