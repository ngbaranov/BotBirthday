import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from settings import settings
from handlers.start import start_router
from handlers.add import add_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск Telegram-бота...")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(add_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка при запуске бота")
    finally:
        await bot.session.close()
        logger.info("Бот завершён")

if __name__ == "__main__":
    asyncio.run(main())