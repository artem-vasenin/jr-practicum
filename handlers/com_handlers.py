from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from config import IMG
from keyboards import kb_start
from classes import ai_client

command_router = Router()

@command_router.message(F.photo)
async def get_photo(message: Message):
    print(message.photo[-1].file_id)

@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    msg = await ai_client.get_text('main')
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=msg,
        reply_markup=kb_start()
    )
