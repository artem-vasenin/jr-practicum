from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import kb_back

kb_router = Router()

@kb_router.message(F.text == 'ChatGPT')
async def kb_chatgpt(message: Message):
    await message.answer(
        text='Will be Chat GPT functionality',
        reply_markup=kb_back(),
    )

# @kb_router.message(F.text == 'Рандомный факт')
# @kb_router.message(Command('random'))
# async def kb_chatgpt(message: Message):
#     await message.answer(
#         text='Will be Chat random fact',
#         reply_markup=kb_back(),
#     )