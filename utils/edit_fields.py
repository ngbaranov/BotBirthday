from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


from dao.dao import BirthdayDAO

# функция в зависимости от выбранного поля, сохраняет новое значение
async def save_single_field(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    field: str,
):
    data = await state.get_data()

    if field == "full_name":
        full_name = message.text.strip()
        await BirthdayDAO(session).update_fields(data["birthday_id"], full_name=full_name)
        await state.clear()
        await message.answer(f"✅ Имя успешно изменено на «{full_name}»")

    elif field == "birth_date":
        try:
            birth_date = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
            await BirthdayDAO(session).update_fields(data["birthday_id"], birth_date=birth_date)
            await state.clear()
            await message.answer(f"✅ Дата успешно изменена на {birth_date.strftime('%d.%m.%Y')}")
        except ValueError:
            await message.answer("⚠️ Неверный формат. Введите дату в формате ДД.ММ.ГГГГ:")

    elif field == "both":
        try:
            text = message.text.replace("\u00A0", " ").strip()
            *name_parts, date_str = text.rsplit(" ", 1)
            full_name = " ".join(name_parts)
            birth_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            await BirthdayDAO(session).update_fields(
                data["birthday_id"],
                full_name=full_name,
                birth_date=birth_date
            )
            await state.clear()
            await message.answer(
                f"✅ Имя и дата успешно изменены на «{full_name} — {birth_date.strftime('%d.%m.%Y')}»"
            )
        except Exception:
            await message.answer("⚠️ Неверный формат. Пример: Иван Иванов 01.01.2001")
