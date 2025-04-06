from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters.callback_data import CallbackData
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Birthday

delete_router = Router()

class DeleteCallback(CallbackData, prefix="delete"):
    birthday_id: int

@delete_router.message(F.text == "Удалить ДР")
async def show_birthdays_for_delete(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    result = await session.execute(select(Birthday).where(Birthday.user_id == user_id))
    birthdays = result.scalars().all()

    if not birthdays:
        await message.answer("У вас нет записей для удаления.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{b.full_name} — {b.birth_date.strftime('%d.%m.%Y')}",
            callback_data=DeleteCallback(birthday_id=b.id).pack()
        )] for b in birthdays
    ])

    await message.answer("Выберите, кого удалить:", reply_markup=kb)

@delete_router.callback_query(DeleteCallback.filter())
async def delete_selected_birthday(
    callback: types.CallbackQuery,
    callback_data: DeleteCallback,
    session: AsyncSession
):
    birthday_id = callback_data.birthday_id
    await session.execute(delete(Birthday).where(Birthday.id == birthday_id))
    await session.commit()

    await callback.message.edit_text("✅ Запись удалена.")
    await callback.answer()
