import json
import os
import logging
from telegram import Update
from telegram.ext import ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = 'bot_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Если файл поврежден или пуст, возвращаем пустую структуру данных
            return {'bot_added_by': {}, 'target_users': {}}
    return {'bot_added_by': {}, 'target_users': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

async def add_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Загружаем данные
    data = load_data()
    
    # Проверяем, является ли пользователь тем, кто добавил бота
    bot_added_by = data['bot_added_by'].get(str(chat_id))
    if user_id != bot_added_by:
        await context.bot.send_message(chat_id=chat_id, text="Только пользователь, добавивший бота, может управлять целевыми пользователями.")
        return
    
    # Проверяем, является ли сообщение ответом на другое сообщение
    if not update.message.reply_to_message:
        await context.bot.send_message(chat_id=chat_id, text="Ответьте командой /clown на сообщение пользователя, которого хотите сделать клоуном.")
        return
    
    try:
        target_user = update.message.reply_to_message.from_user
        if not target_user:
            raise ValueError("Не удалось получить информацию о пользователе")
            
        target_user_id = target_user.id
        target_user_name = target_user.full_name or target_user.username or "Неизвестный пользователь"
        
        # Инициализируем список целевых пользователей для текущего чата, если его нет
        if str(chat_id) not in data['target_users']:
            data['target_users'][str(chat_id)] = []
        
        target_users = data['target_users'][str(chat_id)]
        if target_user_id not in target_users:
            target_users.append(target_user_id)
            save_data(data)
            await context.bot.send_message(chat_id=chat_id, text=f"{target_user_name} стал клоуном 🤡")
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"{target_user_name} уже является клоуном 🤡")
        
        await update.message.delete()
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении целевого пользователя: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Произошла ошибка при обработке команды. Попробуйте еще раз.")

async def remove_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Загружаем данные
    data = load_data()
    
    # Проверяем, является ли пользователь тем, кто добавил бота
    bot_added_by = data['bot_added_by'].get(str(chat_id))
    if user_id != bot_added_by:
        await context.bot.send_message(chat_id=chat_id, text="Только пользователь, добавивший бота, может управлять целевыми пользователями.")
        return
    
    # Проверяем, является ли сообщение ответом на другое сообщение
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id
        target_user_name = target_user.full_name
    else:
        await context.bot.send_message(chat_id=chat_id, text="Ответьте командой /unclown на сообщение пользователя, которого хотите перестать считать клоуном.")
        return
    
    # Проверяем, есть ли список целевых пользователей для этого чата
    if str(chat_id) not in data['target_users']:
        data['target_users'][str(chat_id)] = []
    
    target_users = data['target_users'][str(chat_id)]
    if target_user_id in target_users:
        target_users.remove(target_user_id)
        save_data(data)
        await context.bot.send_message(chat_id=chat_id, text=f"{target_user_name} на некоторое время перестал быть клоуном")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"{target_user_name} не найден в целевых.")
    
    await update.message.delete()

# Обработчик для отслеживания добавления бота в чат
async def track_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.new_chat_members:
            for member in update.message.new_chat_members:
                if member.id == context.bot.id:
                    # Загружаем данные
                    data = load_data()
                    
                    # Сохраняем информацию о том, кто добавил бота
                    data['bot_added_by'][str(update.effective_chat.id)] = update.effective_user.id
                    save_data(data)
                    
                    # Отправляем сообщение о успешной регистрации
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Бот успешно добавлен! Пользователь {update.effective_user.full_name} имеет права управления."
                    )
    except Exception as e:
        logger.error(f"Ошибка при отслеживании добавления бота: {e}") 