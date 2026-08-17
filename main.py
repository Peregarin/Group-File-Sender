import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем настройки из переменных окружения (Bothost)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHAT_ID = os.getenv("SOURCE_CHAT_ID")  # Группа 1 (откуда берем)
DEST_CHAT_ID = os.getenv("DEST_CHAT_ID")      # Группа 2 (куда кидаем)

# Проверка: если забыли вписать токен или ID в Bothost, бот сразу скажет об ошибке
if not all([BOT_TOKEN, SOURCE_CHAT_ID, DEST_CHAT_ID]):
    logger.error("❌ КРИТИЧЕСКАЯ ОШИБКА: Не заданы переменные окружения BOT_TOKEN, SOURCE_CHAT_ID или DEST_CHAT_ID!")
    raise ValueError("Проверьте вкладку 'Переменные' в панели Bothost")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    # 1. ПРОВЕРКА: Сообщение должно быть именно из Группы 1
    if str(message.chat.id) != SOURCE_CHAT_ID:
        return  # Если сообщение из другого чата (или личка) — игнорируем

    # 2. ПРОВЕРКА: Это должен быть документ с расширением .txt
    if message.document and message.document.file_name.lower().endswith(".txt"):
        file_id = message.document.file_id
        file_name = message.document.file_name
        
        # Формируем красивую подпись
        user_name = message.from_user.username or message.from_user.full_name
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
    else:
        # Если файл не .txt или это просто текст — ничего не делаем
        pass

async def main():
    logger.info("🚀 Бот запущен. Жду .txt файлы из Группы 1...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()