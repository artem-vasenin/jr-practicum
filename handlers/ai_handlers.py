from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from openai import AsyncOpenAI
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from config import PROXY_API_TOKEN, PROXY_API
from keyboards import kb_random, kb_back
from utils import get_prompt, get_msg
from config import IMG
from state.state import FSMState
from .com_handlers import com_start

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


@ai_router.message(Command('gpt'))
async def ai_gpt_com(message: Message, state: FSMContext):
    text = await get_msg('gpt')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=text,
        reply_markup=kb_back()
    )
    await state.set_state(FSMState.wait_for_req)

history = {}

@ai_router.message(FSMState.wait_for_req)
async def ai_gpt_req(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await state.clear()
        await com_start(message)
        history.clear()
        return

    prompt = await get_prompt('gpt')
    if message.from_user.id not in history:
        history[message.from_user.id] = [{"role": "system", "content": prompt}]

    history[message.from_user.id].append({"role": "user", "content": message.text})

    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    cmp = await ai_client.chat.completions.create(
        messages=history[message.from_user.id],
        model=AI_MODEL
    )
    caption = cmp.choices[0].message.content
    history[message.from_user.id].append({"role": "assistant", "content": caption})
    await message.answer(
        text=caption,
        reply_markup=kb_back()
    )
