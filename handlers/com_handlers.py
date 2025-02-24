from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from config import IMG
from utils import get_text
from state.state import FSMState
from keyboards import kb_start, kb_back

command_router = Router()

@command_router.message(F.photo)
async def get_photo(message: Message):
    print(message.photo[-1].file_id)

@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    msg = await get_text('main')
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=msg,
        reply_markup=kb_start()
    )

@command_router.message(Command('gpt'))
async def ai_gpt_com(message: Message, state: FSMContext):
    text = await get_text('gpt')
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    await message.answer_photo(
        photo=IMG['GPT'],
        caption=text,
        reply_markup=kb_back()
    )
    await state.set_state(FSMState.wait_for_req)
