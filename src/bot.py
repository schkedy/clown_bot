from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.config import BOT_TOKEN, TIMUR_USER_ID, GOSHA_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text('Бот запущен! Готов ставить клоуна 🤡')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех сообщений"""
    # Проверяем, является ли отправитель целевым пользователем
    if update.message.from_user.id == GOSHA_USER_ID or update.message.from_user.id == TIMUR_USER_ID:
        try:
            # Пробуем поставить реакцию
            
            await update.get_bot().set_message_reaction(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reaction=['🤡'],
                is_big=False
            )
        except Exception as e:
            print(f"Ошибка при установке реакции: {e}")
            # Если не получилось поставить реакцию, отправляем как сообщение
            await update.message.reply_text('🤡')

def main():
    """Основная функция запуска бота"""
    # Создаем приложение 
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 