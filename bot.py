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

"""
Логи выводятся в консоль.
Уровень — INFO.
Для apscheduler убраны лишние подробные логи (оставлены только предупреждения и ошибки).
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def main():
    """
    Создаётся бот с токеном из settings.
    Устанавливается меню.
    Создаётся диспетчер (dp) с хранилищем состояний в памяти.
    :return:
    """
    logger.info("Запуск Telegram-бота...")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await set_main_menu(bot)
    dp = Dispatcher(storage=MemoryStorage(), handle_out_of_scope_messages=True)
    #Подключается middleware для работы с БД.
    dp.update.middleware(DBSessionMiddleware(get_db))
    # Подключается обработчики
    dp.include_router(start_router)
    dp.include_router(text_router)
    dp.include_router(edit_router)
    dp.include_router(add_router)
    dp.include_router(view_router)
    dp.include_router(delete_router)


    # Запускается планировщик задач
    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot, get_db)
    scheduler.start()

    """
    start_polling запускает бота и начинает слушать обновления.
    В случае ошибки выводится лог.
    В конце корректно закрывается сессия бота.
    """
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка при запуске бота")
    finally:
        await bot.session.close()
        logger.info("Бот завершён")

if __name__ == "__main__":
    """
    Запускает асинхронную функцию main()
    """
    asyncio.run(main())