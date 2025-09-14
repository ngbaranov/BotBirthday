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
    """
    Начало процесса редактирования записи о дне рождении.
    Пользователю предлагается выбрать запись для редактирования.
    1. Получаем все записи пользователя из базы данных.
    2. Если записей нет, информируем пользователя.
    3. Если записи есть, отправляем пользователю клавиатуру с выбором записи
    :param message:
    :param session:
    :return:
    """

    birthdays = await BirthdayDAO(session).get_sorted_by_user_id(message.from_user.id)

    if not birthdays:
        await message.answer("У вас пока нет записей для редактирования.")
        return

    await message.answer("Выберите запись, которую хотите изменить:", reply_markup=edit_selection_kb(birthdays))


@edit_router.callback_query(lambda c: c.data and c.data.startswith("edit:"))
async def ask_field_to_edit(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработка выбора записи для редактирования.
    1. Извлекаем ID записи из callback_data.
    2. Сохраняем ID записи в состоянии FSM.
    3. Переходим в состояние выбора поля для редактирования.
    4. Отправляем пользователю клавиатуру с выбором поля для редактирования."""

    birthday_id = int(callback.data.split(":")[1])
    await state.update_data(birthday_id=birthday_id)
    await state.set_state(EditBirthday.choosing_field)
    await callback.message.edit_text("Что будем редактировать?", reply_markup=choose_field_kb())
    await callback.answer()


@edit_router.callback_query(lambda c: c.data and c.data.startswith("field:"), EditBirthday.choosing_field)
async def handle_field_choice(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработка выбора поля для редактирования.
    1. Извлекаем выбранное поле из callback_data.
    2. В зависимости от выбора, переходим в соответствующее состояние FSM.
    3. Запрашиваем у пользователя ввод нового значения для выбранного поля.
    4. Информируем пользователя о текущем состоянии FSM.
    5. Если выбрано некорректное поле, переходим в состояние ожидания обоих полей.
    :param callback:
    :param state:
    :return:
    """
    field = callback.data.split(":")[1]

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
    """
    Обработка нового имени пользователя.
    1. Сохраняем новое имя в базе данных.
    2. Переходим в состояние ожидания нового имени.
    3. Информируем пользователя о текущем состоянии FSM.
    :param message:"""
    await save_single_field(message, state, session, field="full_name")

@edit_router.message(F.text, EditBirthday.waiting_for_new_date)
async def handle_date(message, state, session):
    """
    Обработка новой даты пользователя.
    1. Сохраняем новую дату в базе данных.
    2. Переходим в состояние ожидания новой даты.
    3. Информируем пользователя о текущем состоянии FSM.
    4. Если формат даты неверный, просим ввести дату заново.
    5. Если дата сохранена успешно, очищаем состояние FSM.
    6. Информируем пользователя об успешном изменении даты.
    7. Если выбрано некорректное поле, переходим в состояние ожидания обоих полей.
    8. Информируем пользователя о текущем состоянии FSM.
    :param message:
    :param state:
    :param session:
    :return:
    """
    await save_single_field(message, state, session, field="birth_date")

@edit_router.message(F.text, EditBirthday.waiting_for_all)
async def handle_both(message, state, session):
    """
    Обработка нового имени и даты пользователя.
    1. Сохраняем новое имя и дату в базе данных.
    2. Переходим в состояние ожидания нового имени и даты.
    3. Информируем пользователя о текущем состоянии FSM.
    4. Если формат ввода неверный, просим ввести имя и дату заново.
    5. Если имя и дата сохранены успешно, очищаем состояние FSM.
    6. Информируем пользователя об успешном изменении имени и даты.
    7. Если выбрано некорректное поле, переходим в состояние ожидания обоих полей.

    :param message:
    :param state:
    :param session:
    :return:
    """
    await save_single_field(message, state, session, field="both")
