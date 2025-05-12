import random

from aiogram.types import Message
from aiogram import Router, F

from utils.open_json import birthday_open_json
from keyboards.reply import main_kb


text_router = Router()

@text_router.message(F.text == 'Тексты поздравлений')
async def get_text_birthday(message: Message):
    text = ("\n\n".join(random.sample(birthday_open_json(), 3)) +
            "\n\n" +
            "Если тексты не подходят, нажми на кнопку 👇 Тексты поздравлений")

    await message.answer( text, reply_markup=main_kb())