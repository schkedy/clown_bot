from telegram import Update
from telegram.ext import ContextTypes
from .chat_settings import load_data

async def send_clown_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Загружаем данные
    data = load_data()
    
    # Проверяем, является ли пользователь целевым
    target_users = data['target_users'].get(str(chat_id), [])
    if user_id in target_users:
        # Используем строку с эмодзи вместо ReactionEmoji
        await update.message.set_reaction(['🤡']) 