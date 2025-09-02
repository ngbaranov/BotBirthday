
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, extract

from keyboards.reply import main_kb
from models import Birthday
from datetime import datetime
from zoneinfo import ZoneInfo

import random


from utils.open_json import birthday_open_json



def setup_scheduler(scheduler: AsyncIOScheduler, bot, get_db):
    """Настраивает планировщик задач для проверки дней рождений."""
    @scheduler.scheduled_job("cron", minute="*")
    async def birthday_check():
        """Проверяет, есть ли сегодня дни рождения, и отправляет уведомления."""
        now_moscow = datetime.now(ZoneInfo("Europe/Moscow"))
        if now_moscow.hour == 8 and now_moscow.minute == 15:
            today = now_moscow.date()


            async with get_db() as session:
                """Поиск именинников: Выполняется SQL-запрос к базе данных для поиска всех записей,
                 где день и месяц рождения совпадают с текущей датой"""
                result = await session.execute(
                    select(Birthday).where(
                        extract("day", Birthday.birth_date) == today.day,
                        extract("month", Birthday.birth_date) == today.month
                    )
                )
                birthdays = result.scalars().all()
                # Отправка уведомлений: Для каждого уникального пользователя, у которого есть именинники,
                # отправляется сообщение с поздравлениями и текстами из JSON-файла
                notified_users = set()
                for b in birthdays:
                    if b.user_id not in notified_users:
                        notified_users.add(b.user_id)
                        await bot.send_message(
                            b.user_id,
                            "🎉 Сегодня день рождения у:\n" +
                            "\n".join(f"• {x.full_name}" for x in birthdays if x.user_id == b.user_id) +
                            "\n\n" +
                            "Текст поздравлений:"
                            "\n\n".join(random.sample(birthday_open_json(), 3)) +
                            "\n\n" +
                            "Если тексты не подходят, нажми на кнопку 👇",
                            reply_markup=main_kb()
                        )
