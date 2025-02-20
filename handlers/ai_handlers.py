import os
import httpx
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from openai import AsyncOpenAI
from dotenv import load_dotenv

from config import GPT_TOKEN_TWO, PROXY
from keyboards import kb_back

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ai_router = Router()
ai_client = AsyncOpenAI(
    api_key=GPT_TOKEN_TWO,
    http_client=httpx.AsyncClient(proxy=PROXY)
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