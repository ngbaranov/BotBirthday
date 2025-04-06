from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update
from models import Birthday
from sqlalchemy.ext.asyncio import AsyncSession
from utils.state import EditBirthday
from datetime import datetime

edit_router = Router()

@edit_router.message(F.text == "Редактировать ДР")
async def choose_birthday_to_edit(message: types.Message, session: AsyncSession):
    result = await session.execute(
        select(Birthday).where(Birthday.user_id == message.from_user.id)
    )
    birthdays = result.scalars().all()

    if not birthdays:
        await message.answer("У вас пока нет записей для редактирования.")
        return

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=f"{b.full_name} — {b.birth_date.strftime('%d.%m.%Y')}",
            callback_data=f"edit:{b.id}"
        )] for b in birthdays
    ])

    await message.answer("Выберите запись, которую хотите изменить:", reply_markup=keyboard)

@edit_router.callback_query(lambda c: c.data and c.data.startswith("edit:"))
async def ask_field_to_edit(callback: types.CallbackQuery, state: FSMContext):
    print("➡️ edit: выбран именинник")
    birthday_id = int(callback.data.split(":")[1])
    await state.update_data(birthday_id=birthday_id)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📝 Имя", callback_data="field:name")],
        [types.InlineKeyboardButton(text="📅 Дата", callback_data="field:date")],
        [types.InlineKeyboardButton(text="🔄 Имя и дата", callback_data="field:all")]
    ])

    await state.set_state(EditBirthday.choosing_field)
    await callback.message.edit_text("Что будем редактировать?", reply_markup=keyboard)
    await callback.answer()

@edit_router.callback_query(lambda c: c.data and c.data.startswith("field:"), EditBirthday.choosing_field)
async def handle_field_choice(callback: types.CallbackQuery, state: FSMContext):
    print("➡️ field: выбран тип редактирования")
    field = callback.data.split(":")[1]

    await callback.message.answer(f"➡️ FSM ПЕРЕХОД: выбираем поле {field}")
    current_state = await state.get_state()
    await callback.message.answer(f"🔍 Текущее состояние FSM: {current_state}")

    if field == "name":
        await state.set_state(EditBirthday.waiting_for_new_name)
        await callback.message.answer("Введите новое имя:")
    elif field == "date":
        await state.set_state(EditBirthday.waiting_for_new_date)
        await callback.message.answer("Введите новую дату (ДД.ММ.ГГГГ):")
    else:
        await state.set_state(EditBirthday.waiting_for_all)
        await callback.message.answer("Введите новое имя и дату через пробел (например: Иван Иванов 01.01.2001):")

    await callback.answer()

@edit_router.message(F.text, EditBirthday.waiting_for_new_name)
async def save_new_name(message: types.Message, state: FSMContext, session: AsyncSession):
    print("✅ получено новое имя")
    data = await state.get_data()
    await session.execute(
        update(Birthday)
        .where(Birthday.id == data["birthday_id"])
        .values(full_name=message.text.strip())
    )
    await session.commit()
    await state.clear()

    await message.answer(f"✅ Имя успешно изменено на «{message.text.strip()}»")

@edit_router.message(F.text, EditBirthday.waiting_for_new_date)
async def save_new_date(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        new_date = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
        data = await state.get_data()

        await session.execute(
            update(Birthday)
            .where(Birthday.id == data["birthday_id"])
            .values(birth_date=new_date)
        )
        await session.commit()
        await state.clear()

        await message.answer(f"✅ Дата успешно изменена на {new_date.strftime('%d.%m.%Y')}")

    except ValueError:
        await message.answer("⚠️ Неверный формат. Введите дату в формате ДД.ММ.ГГГГ:")

@edit_router.message(F.text, EditBirthday.waiting_for_all)
async def save_new_name_and_date(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        *name_parts, date_str = message.text.strip().rsplit(" ", 1)
        new_name = " ".join(name_parts)
        new_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        data = await state.get_data()

        await session.execute(
            update(Birthday)
            .where(Birthday.id == data["birthday_id"])
            .values(full_name=new_name, birth_date=new_date)
        )
        await session.commit()
        await state.clear()

        await message.answer(f"✅ Имя и дата успешно изменены на «{new_name} — {new_date.strftime('%d.%m.%Y')}»")

    except ValueError:
        await message.answer("⚠️ Неверный формат. Пример: Иван Иванов 01.01.2001")