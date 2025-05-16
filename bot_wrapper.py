import time
import traceback
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder

# Настройка логов
logging.basicConfig(
    filename='/home/baikhonov/bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация
BOT_TOKEN = "7759262339:AAEd_szhH3dPBvrs7KrWJOOwqxhzEmRxKeg" 
ADMIN_CHAT_ID = 472254624  

def send_alert_to_admin(error_msg: str):
    """Синхронная отправка уведомления админу через run_async"""
    try:
        bot = Bot(token=BOT_TOKEN)
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Используем run_async для синхронного вызова асинхронного метода
        application.run_async(
            bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"🚨 Бот упал:\n{error_msg}"
            )
        )
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления: {e}")

if __name__ == "__main__":
    from dance_bot import main  # Импорт здесь, чтобы избежать циклических зависимостей

    while True:
        try:
            logging.info("🔄 Запуск бота...")
            main()
        except KeyboardInterrupt:
            logging.info("⏹ Бот остановлен вручную")
            break
        except Exception as e:
            error_msg = traceback.format_exc()
            logging.critical(f"💥 Критическая ошибка:\n{error_msg}")
            send_alert_to_admin(error_msg)
            logging.info("⏳ Перезапуск через 10 секунд...")
            time.sleep(10)