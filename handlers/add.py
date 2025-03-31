from aiogram import Router, F
from aiogram.types import Message
from utils.state import waiting_for_birthday
from keyboards.reply import cancel_kb, main_kb
from db.db_depends import get_db
from models import Birthday
from datetime import datetime
from sqlalchemy import insert

add_router = Router()

@add_router.message(F.text == "Добавить ДР")
async def start_adding_birthday(message: Message):
    waiting_for_birthday.add(message.from_user.id)
    await message.answer(
        "Введите ФИО и дату рождения через пробел (например: Иван Петров 1990-05-12)Когда закончите — нажмите «Готово»",
        reply_markup=cancel_kb()
    )

@add_router.message()
async def handle_birthday_input(message: Message):
    user_id = message.from_user.id
    if user_id not in waiting_for_birthday:
        return

    if message.text.lower() in ("готово", "/done"):
        waiting_for_birthday.discard(user_id)
        await message.answer("Вы вышли из режима добавления 👌", reply_markup=main_kb())
        return

    try:
        *name_parts, date_str = message.text.strip().split()
        full_name = " ".join(name_parts)
        birth_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        async for session in get_db():
            await session.execute(
                insert(Birthday).values(
                    user_id=user_id,
                    full_name=full_name,
                    birth_date=birth_date
                )
            )
            await session.commit()

        await message.answer(f"✅ Добавлено: {full_name} — {birth_date}")

    except Exception:
        await message.answer("⚠️ Неверный формат. Пример: Иван Петров 1990-05-12")