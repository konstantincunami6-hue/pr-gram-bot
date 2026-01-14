import telebot
import os
import json
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv('TOKEN') or '8507575219:AAEyv1TiJJbXeDQDHSMs2E-QoRvyuyFrZTw'

bot = telebot.TeleBot(TOKEN)

# Файлы для хранения данных
USERS_FILE = 'users.json'
BALANCE_FILE = 'balances.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_balances(balances):
    with open(BALANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(balances, f, ensure_ascii=False, indent=2)

users = load_users()
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

# Подменю "Пополнить баланс"
def get_topup_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(
        KeyboardButton("90,000 TSugram = 50 ⭐"),
        KeyboardButton("180,000 TSugram = 100 ⭐"),
        KeyboardButton("450,000 TSugram = 250 ⭐"),
        KeyboardButton("1,350,000 TSugram = 750 ⭐"),
        KeyboardButton("2,700,000 TSugram = 1499 ⭐"),
        KeyboardButton("4,500,000 TSugram = 2499 ⭐")
    )
    keyboard.add(KeyboardButton("⭐ Другая сумма"))
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard

# Подменю "Мои задания"
def get_tasks_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(
        KeyboardButton("Проверка выполненных заданий (реакции)"),
        KeyboardButton("Проверка выполненных заданий (боты)")
    )
    keyboard.add(KeyboardButton("Создать новое задание +"))
    keyboard.add(KeyboardButton("🔙 Назад в кабинет"))
    return keyboard

# Подменю "Создать новое задание +"
def get_create_task_keyboard():
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

# Клавиатура для реферальной системы
def get_referral_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("📤 Поделиться ссылкой"))
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard

# Клавиатура для проверки заданий
def get_check_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("🔙 Назад в Мои задания"))
    return keyboard

# Клавиатура для ОП
def get_op_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("Добавить бота в чат"))
    keyboard.add(KeyboardButton("Добавить бота в канал"))
    keyboard.add(KeyboardButton("Чат поддержки"))
    keyboard.add(KeyboardButton("🔙 Назад"))
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
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    # Реферальный параметр
    ref_id = None
    if len(message.text.split()) > 1:
        ref_id = message.text.split()[1]

    if ref_id and ref_id != user_id and ref_id in users:
        if ref_id not in balances:
            balances[ref_id] = 0
        balances[ref_id] += 5000
        save_balances(balances)
        try:
            bot.send_message(ref_id, "Вам начислено 5000 TSugram за нового реферала! 🎉")
        except:
            pass

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

    if text == "📊 Мой кабинет":
        balance = balances.get(user_id, 0)
        cabinet_text = f"""
Ваш кабинет:

🔑 Мой ID: {user_id}
💰 Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, cabinet_text, reply_markup=get_cabinet_keyboard())

    elif text == "💰 Пополнить баланс":
        topup_text = """
Если возникли проблемы с пополнением — обращайтесь: @Tsunami_TG

Введите сумму пополнения в TSugram
или выберите:
        """.strip()

        bot.send_message(message.chat.id, topup_text, reply_markup=get_topup_keyboard())

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

    elif text == "🎒 Мои задания":
        tasks_text = """
Нажмите на кнопки, чтобы выбрать задание

⚠️ Запрещено отписываться ранее чем через 7 дней от групп

В противном случае ваша возможность выполнять задания будет заблокирована, а заработанные средства аннулированы.

Здесь вы можете управлять своими заданиями
        """.strip()

        bot.send_message(message.chat.id, tasks_text, reply_markup=get_tasks_keyboard())

    elif text == "Проверка выполненных заданий (реакции)":
        unchecked = 0  # Для теста поменяй на число
        check_text = "✅ Все выполнения проверены" if unchecked == 0 else f"У вас не проверено {unchecked} заданий"
        bot.send_message(message.chat.id, check_text, reply_markup=get_check_keyboard())

    elif text == "Проверка выполненных заданий (боты)":
        unchecked = 0
        check_text = "✅ Все выполнения проверены" if unchecked == 0 else f"У вас не проверено {unchecked} заданий"
        bot.send_message(message.chat.id, check_text, reply_markup=get_check_keyboard())

    elif text == "Создать новое задание +":
        create_task_text = """
Что вы хотите рекламировать?

💰 Баланс: 0 TSugram
        """.strip()

        bot.send_message(message.chat.id, create_task_text, reply_markup=get_create_task_keyboard())

    elif text == "🔊 ОП (Проверка подписки)":
        op_text = """
✅ *Функция проверки подписки на канал/чат*

▸ *Шаг 1.* Добавьте бота в ваш чат с правами администратора.  
   (Можно с помощью этой ссылки: t.me/TSUGRAM_PRBOT?startgroup=true)

▸ *Шаг 2.* Добавьте бота в администраторы канала/чата, на который хотите установить проверку подписки.  
   Вы можете передать эту ссылку администратору канала/чата.

*Шаг 3.* Чтобы включить подписку на канал/чат, напишите в вашем чате команду:  
`/setup` ссылка_или_@username  

Пример:  
`/setup @prgram_channel`  
`/setup -1001234567890`

⛔️ *Чтобы отключить функцию, вам нужно:*  
Написать команду:  
`/unsetup` ссылка (чата/канала, для которого хотите прекратить проверку)  
Пример: `/unsetup @rove`

➕ *Максимальное количество одновременной проверки* — 5 каналов/чатов

❌ *Для отключения сразу всех установленных проверок* на подписки используйте команду:  
`/unsetup all`

💡 Напишите команду `/status` в вашем чате, чтобы получить перечень активных проверок на подписку, а также информацию о времени действия каждой проверки и ее отмене.

🕒 *Дополнительно вы можете установить таймер* для автоматического отключения проверки подписки.  
Пример:  
`/setup @rove 1d`

Время можно указать в секундах, минутах, часах и днях:  
s — секунд  
m — минут  
h — часов  
d — дней

Если возникли сложности, обращайтесь в чат поддержки  
@Tsunami_TG
        """.strip()

        bot.send_message(message.chat.id, op_text, parse_mode='Markdown', reply_markup=get_op_keyboard())

    elif text == "📢 Рекламировать":
        balance = balances.get(user_id, 0)
        advertise_text = f"""
Что вы хотите рекламировать?

💰 Баланс: {balance} TSugram
        """.strip()

        bot.send_message(message.chat.id, advertise_text, reply_markup=get_advertise_keyboard())

    elif text == "Канал":
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

    # Навигация "Назад"
    elif text in ["🔙 Назад", "← Назад", "🔙 Назад в Мои задания"]:
        bot.send_message(message.chat.id, "Вы вернулись в предыдущее меню 👇", reply_markup=get_main_keyboard())

    elif text == "🔙 Назад в кабинет":
        bot.send_message(message.chat.id, "Вы вернулись в Мой кабинет 👇", reply_markup=get_cabinet_keyboard())

    elif text == "🔙 Назад в главное меню":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню 👇", reply_markup=get_main_keyboard())

    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню 👇", reply_markup=get_main_keyboard())

print("Бот запущен — кнопка ОП и все остальные работают!")
bot.infinity_polling()
