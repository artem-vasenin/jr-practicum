from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from openai import AsyncOpenAI

from config import PROXY_API_TOKEN, PROXY_API
from keyboards import kb_back

ai_router = Router()
ai_client = AsyncOpenAI(
    api_key=PROXY_API_TOKEN,
    base_url=PROXY_API
)

@ai_router.message(F.text == 'Рандомный факт')
@ai_router.message(Command('random'))
async def ai_random(message: Message):
    cmp = await ai_client.chat.completions.create(
        messages=[{'role': 'user', 'content': 'Напиши рандомный факт'}],
        model='gpt-3.5-turbo'
    )
    for i in dict(cmp).items():
        print(i)
    # await message.answer(
    #     text='Will be Chat random fact',
    #     reply_markup=kb_back(),
    # )