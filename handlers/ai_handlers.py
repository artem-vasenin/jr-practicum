from aiogram import F, Router
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import IMG
from utils import get_text
from classes import ai_client
from .com_handlers import com_start
from keyboards import kb_random, kb_back
from state.state import FSMState, TalkState


ai_router = Router()
history = {}

@ai_router.message(F.text == 'Рандомный факт')
@ai_router.message(F.text == 'Хочу еще факт!')
@ai_router.message(Command('random'))
async def ai_random(message: Message):
    prompt = await get_text('random', is_prompt=True)
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request([], prompt)
    await message.answer_photo(
        photo=IMG['random'],
        caption=caption,
        reply_markup=kb_random()
    )

@ai_router.message(FSMState.wait_for_req)
async def ai_gpt_req(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await state.clear()
        await com_start(message)
        history.clear()
        return

    if message.from_user.id not in history:
        prompt = await get_text('gpt', is_prompt=True)
        history[message.from_user.id] = [{"role": "system", "content": prompt}]

    history[message.from_user.id].append({"role": "user", "content": message.text})
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request(history[message.from_user.id], '')
    history[message.from_user.id].append({"role": "assistant", "content": caption})
    await message.answer(text=caption, reply_markup=kb_back())


@ai_router.message(TalkState.wait_for_answer)
async def ai_gpt_talk(message: Message, state: FSMContext):
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    data = await state.get_data()
    data['dialog'].append({'role': 'user', 'content': message.text})
    caption = await ai_client.text_request(data['dialog'], '')
    data['dialog'].append({'role': 'assistant', 'content': caption})
    await state.update_data(dialog=data['dialog'])
    await message.answer(text=caption, reply_markup=kb_back())

@ai_router.callback_query(F.data.startswith('quiz_'))
async def get_question(cb: CallbackQuery):
    print(cb.data)
