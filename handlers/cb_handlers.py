from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import IMG
from keyboards import kb_back, TalkPerson

cb_router = Router()

@cb_router.callback_query(TalkPerson.filter(F.button == 'tk'))
async def select_person(cb: CallbackQuery, callback_data: TalkPerson):
    await cb.bot.send_photo(
        chat_id=cb.from_user.id,
        photo=IMG[callback_data.file_name],
        caption=f'Вас приветствует {callback_data.name}, пообщаемся?',
        reply_markup=kb_back()
    )