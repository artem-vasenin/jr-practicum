from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import IMG
from utils import get_text
from state.state import TalkState
from keyboards import kb_back, TalkPerson


cb_router = Router()

@cb_router.callback_query(TalkPerson.filter(F.button == 'tk'))
async def select_person(cb: CallbackQuery, callback_data: TalkPerson, state: FSMContext):
    prompt = await get_text(callback_data.file_name, is_prompt=True)
    await state.clear()
    await state.set_state(TalkState.wait_for_answer)
    await state.update_data(
        name=callback_data.name,
        f_name=callback_data.file_name,
        dialog=[{'role': 'system', 'content': prompt}],
    )
    await cb.bot.send_photo(
        chat_id=cb.from_user.id,
        photo=IMG[callback_data.file_name],
        caption=f'Вас приветствует {callback_data.name}, пообщаемся?',
        reply_markup=kb_back(),
    )
