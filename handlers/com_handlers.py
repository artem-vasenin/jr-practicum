from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import kb_start

command_router = Router()

@command_router.message(F.photo)
async def get_photo(message: Message):
    ...

@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    await message.answer(text=f'Hello, {message.from_user.username}!', reply_markup=kb_start())
