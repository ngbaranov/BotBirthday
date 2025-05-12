from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Как пользоваться"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())