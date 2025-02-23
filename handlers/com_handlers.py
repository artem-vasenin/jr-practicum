from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import kb_start
from config import IMG
from utils import get_msg

command_router = Router()

@command_router.message(F.photo)
async def get_photo(message: Message):
    print(message.photo[-1].file_id)

@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    msg = await get_msg('main')
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=msg,
        reply_markup=kb_start()
    )
