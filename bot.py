import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboards.main import set_main_menu
from scheduler import setup_scheduler
from settings import settings
from handlers.start import start_router
from handlers.add import add_router
from handlers.view import view_router
from handlers.delete import delete_router
from handlers.edit import edit_router
from handlers.get_text_birthday import text_router
from middlewares.db_session import DBSessionMiddleware
from db.db_depends import get_db
from db.db import async_sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск Telegram-бота...")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await set_main_menu(bot)
    dp = Dispatcher(storage=MemoryStorage(), handle_out_of_scope_messages=True)

    dp.update.middleware(DBSessionMiddleware(get_db))

    dp.include_router(start_router)
    dp.include_router(text_router)
    dp.include_router(edit_router)
    dp.include_router(add_router)
    dp.include_router(view_router)
    dp.include_router(delete_router)



    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot, get_db)
    scheduler.start()


    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка при запуске бота")
    finally:
        await bot.session.close()
        logger.info("Бот завершён")

if __name__ == "__main__":
    asyncio.run(main())