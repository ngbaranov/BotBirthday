from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_kb():
    kb_list = [
        [KeyboardButton(text="Добавить ДР"), KeyboardButton(text="Просмотр ДР")],
        [KeyboardButton(text="Редактировать ДР"), KeyboardButton(text="Удалить ДР")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Готово")]],
        resize_keyboard=True
    )