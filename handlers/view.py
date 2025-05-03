import calendar
from collections import defaultdict
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from dao.dao import BirthdayDAO
from schemas.birthday import BirthdayOut

view_router = Router()

@view_router.message(F.text == "Просмотр ДР")
async def view_birthdays(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    birthdays = await BirthdayDAO(session).get_sorted_by_user_id(user_id)

    if not birthdays:
        await message.answer("❌ У вас пока нет добавленных дней рождений.")
        return

    # Преобразуем в Pydantic-модели
    birthdays_out = [BirthdayOut.model_validate(b, from_attributes=True) for b in birthdays]

    # Группируем по месяцам
    grouped = defaultdict(list)
    for b in birthdays_out:
        grouped[b.birth_date.month].append(b)

    MONTHS_RU = ["", "Январь", "Февраль", "Март", "Апрель", "Май",
                 "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    text = "🎉 Ваши дни рождения (начиная с ближайших):\n\n"
    for month in sorted(grouped.keys(), key=lambda m: (m < date.today().month, m)):
        text += f"📅 {MONTHS_RU[month]}:\n"
        for b in grouped[month]:
            text += f"• {b.full_name} — {b.birth_date.strftime('%d.%m.%Y')}\n"
        text += "\n"

    await message.answer(text.strip())
