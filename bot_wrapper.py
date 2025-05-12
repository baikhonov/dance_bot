import time
import traceback

# Импортируем main() из вашего основного файла бота
from dance_bot import main

if __name__ == "__main__":
    while True:
        try:
            print("🔁 Запуск бота...")
            main()
        except Exception as e:
            print("❌ Бот упал с ошибкой:")
            traceback.print_exc()
            print("⏳ Перезапуск через 10 секунд...")
            time.sleep(10)
