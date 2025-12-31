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

# Подменю "Мои задания"
def get_tasks_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(
        KeyboardButton("Проверка выполненных заданий (реакции)"),
        KeyboardButton("Проверка выполненных заданий (боты)")
    )
    keyboard.add(KeyboardButton("Создать новое задание +"))
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

    elif text == "🎒 Мои задания":
        tasks_text = """
Нажмите на кнопки, чтобы выбрать задание

⚠️ Запрещено отписываться ранее чем через 7 дней от групп

В противном случае ваша возможность выполнять задания будет заблокирована, а заработанные средства аннулированы.

Здесь вы можете управлять своими заданиями
        """.strip()

        bot.send_message(message.chat.id, tasks_text, reply_markup=get_tasks_keyboard())

    elif text == "🔙 Назад" or text == "🔙 Назад в меню":
        bot.send_message(message.chat.id, "Вы вернулись в предыдущее меню 👇", reply_markup=get_main_keyboard() if text == "🔙 Назад в меню" else get_cabinet_keyboard())

    elif text in ["💰 Пополнить баланс", "👥 Реферальная система", "📈 Уровневая система", "🌐 Изменить язык", "❌ Отключить уведомления", "💰 Заработать", "📢 Рекламировать", "🧾 Чеки", "🔊 ОП (Проверка подписки)", "🤖 Наши боты / Статистика", "🔗 Полезные ссылки", "📝 Инструкция"]:
        bot.send_message(message.chat.id, "Эта функция в разработке 🚧", reply_markup=get_cabinet_keyboard() if text in ["💰 Пополнить баланс", "👥 Реферальная система", "📈 Уровневая система", "🌐 Изменить язык", "❌ Отключить уведомления"] else get_main_keyboard())

    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню 👇", reply_markup=get_main_keyboard())

print("Бот PR GRAM с 'Мои задания' успешно запущен!")
bot.infinity_polling()
