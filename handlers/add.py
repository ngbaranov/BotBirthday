from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from utils.state import waiting_for_birthday
from keyboards.reply import cancel_kb, main_kb
from models import Birthday
from dao.dao import BirthdayDAO
from schemas.birthday import BirthdayCreate

add_router = Router()


@add_router.message(F.text == "Добавить ДР")
async def start_adding_birthday(message: Message):
    waiting_for_birthday.add(message.from_user.id)
    await message.answer(
        "Введите ФИО и дату рождения через пробел (например: Иван Петров 12.05.2000) \n Когда закончите — нажмите «Готово»",
        reply_markup=cancel_kb()
    )


@add_router.message(~F.text.in_({"Просмотр ДР", "Редактировать ДР", "Удалить ДР"}))
async def handle_birthday_input(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    if user_id not in waiting_for_birthday:
        return False

    if message.text.lower() in ("готово", "/done"):
        waiting_for_birthday.discard(user_id)
        await message.answer("Вы вышли из режима добавления 👌", reply_markup=main_kb())
        return

    try:
        text = message.text.replace("\u00A0", " ").strip()
        *name_parts, date_str = text.rsplit(" ", 1)
        full_name = " ".join(name_parts)
        birth_date = datetime.strptime(date_str, "%d.%m.%Y").date()

        birthday_data = BirthdayCreate(
            user_id=user_id,
            full_name=full_name,
            birth_date=birth_date
        )

        await BirthdayDAO(session).add(birthday_data)
        await message.answer(f"✅ Добавлено: {full_name} — {birth_date.strftime('%d.%m.%Y')}")

    except Exception:
        await message.answer("⚠️ Неверный формат. Пример: Иван Петров 12.03.1990")

