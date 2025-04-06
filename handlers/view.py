from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from models import Birthday
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

view_router = Router()

@view_router.message(F.text == "Просмотр ДР")
async def view_birthdays(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    result = await session.execute(
        select(Birthday)
        .where(Birthday.user_id == user_id)
        .order_by(Birthday.birth_date)
    )

    birthdays = result.scalars().all()

    if not birthdays:
        await message.answer("❌ У вас пока нет добавленных дней рождений.")
        return

    text = "🎉 Ваши дни рождения:\n\n"
    for person in birthdays:
        text += f"• {person.full_name} — {person.birth_date.strftime('%d.%m.%Y')}\n"

    await message.answer(text)
