from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import main_kb
import logging

logger = logging.getLogger(__name__)
start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info("🔥 Хендлер /start сработал")
    await message.answer("Привет! Я бот 👋", reply_markup=main_kb())