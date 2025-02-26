from bot.handlers.chat_settings import add_target_user, remove_target_user, track_bot_added
from bot.handlers.reactions import send_clown_reaction
from bot.config.config import BOT_TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 