import random

from aiogram.types import Message
from aiogram import Router, F

from utils.open_json import birthday_open_json
from utils.grattersAI import generate_birthday_text
from keyboards.reply import main_kb


text_router = Router()

@text_router.message(F.text == 'Тексты поздравлений')
async def get_text_birthday(message: Message):
    # text = ("\n\n".join(random.sample(birthday_open_json(), 3)) +
    #         "\n\n" +
    #         "Если тексты не подходят, нажми на кнопку 👇 Тексты поздравлений")
    #
    # await message.answer( text, reply_markup=main_kb())

    loading_message = await message.answer("Генерирую поздравления... ⏳")

    try:
        # Генерируем поздравления через OpenAI
        birthday_texts = await generate_birthday_text()
        # Формируем итоговый текст
        text = ("\n\n".join(birthday_texts) +
                "\n\n" +
                "Если тексты не подходят, нажми на кнопку 👇 Тексты поздравлений")

        # Удаляем сообщение о загрузке
        await loading_message.delete()

        # Отправляем сгенерированные поздравления
        await message.answer(text, reply_markup=main_kb())

    except Exception as e:
        # Удаляем сообщение о загрузке в случае ошибки
        await loading_message.delete()

        # Отправляем сообщение об ошибке
        await message.answer(
            "Произошла ошибка при генерации поздравлений. Попробуйте еще раз.",
            reply_markup=main_kb()
        )