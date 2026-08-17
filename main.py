import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен берем из системы
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Хардкодим ID чатов как числа (без кавычек)
SOURCE_CHAT_ID = -76935771164039
DEST_CHAT_ID = -73576057572743

# ПРОВЕРКА УДАЛЕНА

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    # 1. ПРОВЕРКА: Сообщение должно быть именно из Группы 1
    # Сравниваем напрямую числа (chat.id возвращает число)
    if message.chat.id != SOURCE_CHAT_ID:
        return

    # 2. ПРОВЕРКА: Это должен быть документ с расширением .txt
    # Добавил безопасную проверку имени файла, чтобы не было ошибок на пустых документах
    if message.document and message.document.file_name and message.document.file_name.lower().endswith(".txt"):
        file_id = message.document.file_id
        file_name = message.document.file_name
        
        # Безопасное формирование подписи
        if message.from_user:
            user_name = message.from_user.username or message.from_user.full_name
        else:
            user_name = "Неизвестный отправитель"
            
        caption = f"📄 Файл: <b>{file_name}</b>\n👤 От: @{user_name}"

        logger.info(f"Пересылаю файл {file_name} из {SOURCE_CHAT_ID} в {DEST_CHAT_ID}")

        try:
            await bot.send_chat_action(chat_id=DEST_CHAT_ID, action="upload_document")
            await bot.send_document(
                chat_id=DEST_CHAT_ID,
                document=file_id,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
            logger.info("✅ Файл успешно переслан!")
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке файла: {e}")

async def main():
    logger.info("🚀 Бот запущен! Жду .txt файлы...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())