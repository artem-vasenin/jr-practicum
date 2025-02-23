from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from openai import AsyncOpenAI

from config import PROXY_API_TOKEN, PROXY_API
from keyboards import kb_random
from utils import get_prompt
from config import IMG

ai_router = Router()
ai_client = AsyncOpenAI(
    api_key=PROXY_API_TOKEN,
    base_url=PROXY_API,
)
AI_MODEL = 'gpt-3.5-turbo' # 'gpt-4o' дорогой гад


@ai_router.message(F.text == 'Рандомный факт')
@ai_router.message(F.text == 'Хочу еще факт!')
@ai_router.message(Command('random'))
async def ai_random(message: Message):
    prompt = await get_prompt('random')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    cmp = await ai_client.chat.completions.create(
        messages=[{'role': 'system', 'content': prompt}],
        model=AI_MODEL
    )
    caption = cmp.choices[0].message.content
    await message.answer_photo(
        photo=IMG['RANDOM'],
        caption=caption,
        reply_markup=kb_random()
    )
