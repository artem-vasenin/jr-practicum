from aiogram import F, Router
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import IMG
from utils import get_text
from classes import ai_client
from .com_handlers import com_start
from keyboards import kb_random, kb_back, kb_quiz
from state.state import FSMState, TalkState, QuizState


ai_router = Router()
gptHistory = {}
quizHistory = {}

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
        gptHistory.clear()
        return

    if message.from_user.id not in gptHistory:
        prompt = await get_text('gpt', is_prompt=True)
        gptHistory[message.from_user.id] = [{"role": "system", "content": prompt}]

    gptHistory[message.from_user.id].append({"role": "user", "content": message.text})
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request(gptHistory[message.from_user.id], '')
    gptHistory[message.from_user.id].append({"role": "assistant", "content": caption})
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

@ai_router.message(QuizState.wait_for_answer)
async def get_question(message: Message, state: FSMContext):
    if message.text == 'Python':
        user_q = 'quiz_prog'
    elif message.text == 'Биология':
        user_q = 'quiz_biology'
    elif message.text == 'Математика':
        user_q = 'quiz_math'
    elif message.text == 'Ещё вопрос':
        user_q = 'quiz_more'
    else:
        user_q = message.text
    data = await state.get_data()
    data['dialog'].append({'role': 'user', 'content': user_q})
    right = data['right']
    wrong = data['wrong']
    await message.bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    caption = await ai_client.text_request(data['dialog'], '')
    data['dialog'].append({'role': 'assistant', 'content': caption})

    if caption.startswith('Правильно!'):
        right += 1
        caption += f' (Правильных ответов: {right}, неправильных: {wrong})'
    elif caption.startswith('Неправильно!'):
        wrong += 1
        caption += f' (Правильных ответов: {right}, неправильных: {wrong})'

    await state.update_data(dialog=data['dialog'], right=right, wrong=wrong)
    res = await message.answer(text=caption, reply_markup=kb_quiz())
