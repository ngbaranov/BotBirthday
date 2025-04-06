from aiogram.fsm.state import StatesGroup, State

waiting_for_birthday = set()

class EditBirthday(StatesGroup):
    choosing_field = State()
    waiting_for_new_name = State()
    waiting_for_new_date = State()
    waiting_for_all = State()