from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from models import Birthday

def edit_selection_kb(birthdays: list[Birthday]) -> InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup для выбора записи о дне рождении для редактирования."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{b.full_name} — {b.birth_date.strftime('%d.%m.%Y')}",
                    callback_data=f"edit:{b.id}"
                )
            ] for b in birthdays
        ]
    )

def choose_field_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Имя", callback_data="field:name")],
            [InlineKeyboardButton(text="📅 Дата", callback_data="field:date")],
            [InlineKeyboardButton(text="🔄 Имя и дата", callback_data="field:all")]
        ]
    )


