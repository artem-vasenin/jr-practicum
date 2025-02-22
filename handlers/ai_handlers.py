from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from openai import AsyncOpenAI

from config import PROXY_API_TOKEN, PROXY_API
from keyboards import kb_random

ai_router = Router()
ai_client = AsyncOpenAI(
    api_key=PROXY_API_TOKEN,
    base_url=PROXY_API
)

@ai_router.message(F.text == 'Рандомный факт')
@ai_router.message(F.text == 'Хочу еще факт!')
@ai_router.message(Command('random'))
async def ai_random(message: Message):
    cmp = await ai_client.chat.completions.create(
        messages=[{'role': 'user', 'content': 'Напиши рандомный факт'}],
        # model='gpt-4o' # дорогой гад
        model='gpt-3.5-turbo'
    )
    caption = cmp.choices[0].message.content
    await message.answer(
        text=caption,
        reply_markup=kb_random(),
    )