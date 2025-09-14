import random

from aiogram.types import Message
from aiogram import Router, F

from utils.open_json import birthday_open_json
from utils.grattersAI import generate_birthday_text
from keyboards.reply import main_kb


text_router = Router()

@text_router.message(F.text == 'Тексты поздравлений')
async def get_text_birthday(message: Message):
    """
    Обрабатывает команду "Тексты поздравлений".
    Генерирует и отправляет пользователю 3 поздравления из парсинга и 1 от ИИ.
    :param message: Объект сообщения от пользователя.
    """
    loading_message = await message.answer("Генерирую поздравления... ⏳")

    try:
        # Получаем 3 поздравления из парсинга
        parsed_texts = random.sample(birthday_open_json(), 3)
        # Получаем поздравление с помощью ИИ
        ai_text_raw = await generate_birthday_text()
        # Извлекаем первый элемент из списка и убираем \n
        ai_text_clean = ai_text_raw[0].replace('\\n', '\n') if ai_text_raw else ""
        ai_texts = [f'🤖 <b>Поздравление от ИИ:</b>\n{ai_text_clean}']

        # Объединяем все поздравления
        all_texts = parsed_texts + ai_texts

        text = (
            "\n\n".join(all_texts) +
            "\n\n" +
            "Если тексты не подходят, нажми на кнопку 👇 Тексты поздравлений"
        )

        await loading_message.delete()
        await message.answer(text, reply_markup=main_kb(), parse_mode="HTML")

    except Exception as e:
        await loading_message.delete()
        await message.answer(
            "Произошла ошибка при генерации поздравлений. Попробуйте еще раз.",
            reply_markup=main_kb())