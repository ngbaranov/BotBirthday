from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import main_kb
import logging

logger = logging.getLogger(__name__)
start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: Message):
    """Обрабатывает команду /start.
    Отправляет приветственное сообщение и основную информацию о боте."""
    logger.info("🔥 Хендлер /start сработал")
    text = f"Привет, {message.from_user.first_name}!👋\n\nЯ венец творения, одного гениального программиста.\n\nТак как "\
           "я решил помочь тебе и буду заниматься организацией дней рождений твоих кожаных друзей\n\n"\
            "Я умею:\n" \
            "1️⃣ Добавлять дни рождений\n" \
            "2️⃣ Просматривать дни рождений\n" \
            "3️⃣ Удалять дни рождений\n" \
            "4️⃣ Редактировать дни рождений\n" \
            "5️⃣ Генерировать тексты поздравлений\n\n"\
            "Также я умею напоминать о днях рождений:\n\n" \
            "Если что-то не работает, нажми на кнопку старт в меню бургер,\
             внизу слева, если после этого не помогло, то три точки в правом верхнем углу->Очистить историю->галочка у бота тоже\n\n" \
            "Нажми на одну из кнопок внизу.👇\n\n"\

    await message.answer(text, reply_markup=main_kb())