from handlers.chat_settings import add_target_user, remove_target_user, track_bot_added
from bot.handlers.reactions import send_clown_reaction
from bot.config.config import BOT_TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text('Бот запущен! Готов ставить клоуна 🤡')

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler('clown', add_target_user))
    application.add_handler(CommandHandler('unclown', remove_target_user))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_bot_added))
    
    # Добавляем обработчик для реакций
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_clown_reaction))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка при обработке обновления: {context.error}")
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Произошла ошибка при обработке команды. Попробуйте еще раз."
        )

if __name__ == '__main__':
    main() 