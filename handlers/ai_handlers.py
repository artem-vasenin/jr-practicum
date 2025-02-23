from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from keyboards import kb_random, kb_back
from config import IMG
from state.state import FSMState
from .com_handlers import com_start
from classes import ai_client

ai_router = Router()
history = {}

@ai_router.message(F.text == 'Рандомный факт')
@ai_router.message(F.text == 'Хочу еще факт!')
@ai_router.message(Command('random'))
async def ai_random(message: Message):
    prompt = await ai_client.get_text('random', is_prompt=True)
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request([], prompt)
    await message.answer_photo(
        photo=IMG['RANDOM'],
        caption=caption,
        reply_markup=kb_random()
    )


@ai_router.message(Command('gpt'))
async def ai_gpt_com(message: Message, state: FSMContext):
    text = await ai_client.get_text('gpt')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=text,
        reply_markup=kb_back()
    )
    await state.set_state(FSMState.wait_for_req)

@ai_router.message(FSMState.wait_for_req)
async def ai_gpt_req(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await state.clear()
        await com_start(message)
        history.clear()
        return

    prompt = await ai_client.get_text('gpt', is_prompt=True)
    if message.from_user.id not in history:
        history[message.from_user.id] = [{"role": "system", "content": prompt}]

    history[message.from_user.id].append({"role": "user", "content": message.text})

    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request(history[message.from_user.id], '')
    history[message.from_user.id].append({"role": "assistant", "content": caption})
    await message.answer(
        text=caption,
        reply_markup=kb_back()
    )
