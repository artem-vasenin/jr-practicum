from aiogram import F, Router
from aiogram.types import Message

from keyboards import kb_back

kb_router = Router()

@kb_router.message(F.text == 'ChatGPT')
async def kb_chatgpt(message: Message):
    await message.answer(
        text='Will be Chat GPT functionality',
        reply_markup=kb_back(),
    )