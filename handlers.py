from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command


command_router = Router()

@command_router.message(Command('start'))
async def com_start(message: Message):
    for i in dict(message).items():
        print(i)
