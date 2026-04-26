import logging

from bot.app import create_application


logger = logging.getLogger(__name__)


def main():
    """Запуск бота."""
    application = create_application()
    logger.info("Запуск бота...")
    try:
        application.run_polling()
    except Exception as error:
        logger.error("Бот остановлен с ошибкой: %s", error)
        raise


if __name__ == "__main__":
    main()
