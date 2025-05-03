from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


from utils.state import EditBirthday
from utils.edit_fields import save_single_field
from keyboards.inline import edit_selection_kb, choose_field_kb
from dao.dao import BirthdayDAO

edit_router = Router()


@edit_router.message(F.text == "Редактировать ДР")
async def choose_birthday_to_edit(message: types.Message, session: AsyncSession):

    birthdays = await BirthdayDAO(session).get_sorted_by_user_id(message.from_user.id)

    if not birthdays:
        await message.answer("У вас пока нет записей для редактирования.")
        return

    await message.answer("Выберите запись, которую хотите изменить:", reply_markup=edit_selection_kb(birthdays))


@edit_router.callback_query(lambda c: c.data and c.data.startswith("edit:"))
async def ask_field_to_edit(callback: types.CallbackQuery, state: FSMContext):
    print("➡️ edit: выбран именинник")
    birthday_id = int(callback.data.split(":")[1])
    await state.update_data(birthday_id=birthday_id)
    await state.set_state(EditBirthday.choosing_field)
    await callback.message.edit_text("Что будем редактировать?", reply_markup=choose_field_kb())
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
async def handle_name(message, state, session):
    await save_single_field(message, state, session, field="full_name")

@edit_router.message(F.text, EditBirthday.waiting_for_new_date)
async def handle_date(message, state, session):
    await save_single_field(message, state, session, field="birth_date")

@edit_router.message(F.text, EditBirthday.waiting_for_all)
async def handle_both(message, state, session):
    await save_single_field(message, state, session, field="both")
