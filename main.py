import os
import time
import logging

# Настройка логов, чтобы видеть их в панели Bothost
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Бот Group File Sender запущен на Bothost!")
    logger.info("✅ Ожидание обновлений от MAX...")
    
    # Бесконечный цикл, чтобы процесс не завершался
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
