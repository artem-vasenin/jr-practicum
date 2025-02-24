from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from config import IMG
from utils import get_text
from state.state import FSMState
from keyboards import kb_start, kb_back, kb_talk

command_router = Router()

@command_router.message(F.photo)
async def get_photo(message: Message):
    print(message.photo[-1].file_id)

@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    msg = await get_text('main')
    await message.answer_photo(
        photo=IMG['gpt'],
        caption=msg,
        reply_markup=kb_start()
    )

@command_router.message(F.text == 'Диалог с GPT')
@command_router.message(Command('gpt'))
async def ai_gpt_com(message: Message, state: FSMContext):
    text = await get_text('gpt')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    await message.answer_photo(
        photo=IMG['gpt'],
        caption=text,
        reply_markup=kb_back()
    )
    await state.set_state(FSMState.wait_for_req)

@command_router.message(F.text == 'Диалог с личностью')
@command_router.message(Command('talk'))
async def ai_gpt_com(message: Message, state: FSMContext):
    text = await get_text('talk')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    await message.answer_photo(
        photo=IMG['talk'],
        caption=text,
        reply_markup=kb_talk()
    )
    # await state.set_state(FSMState.wait_for_req)
