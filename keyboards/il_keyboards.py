import os

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TalkPerson(CallbackData, prefix='tk'):
    button: str
    name: str
    file_name: str

def kb_talk():
    keyboard = InlineKeyboardBuilder()
    files = [f for f in os.listdir('resources/prompts') if f.startswith('talk_')]
    names = []
    for f in files:
        with open(os.path.join('resources/prompts', f), 'r', encoding='UTF-8') as file:
            names.append(file.read().split(',', 1)[0][5:])
    btns = zip(files, names)
    for f in btns:
        keyboard.button(
            text=f[1],
            callback_data=TalkPerson(
                button='tk',
                name=f[1],
                file_name=f[0].rsplit('.')[0]
            )
        )
    keyboard.adjust(*[1]*len(files))
    return keyboard.as_markup(resize_keyboard=True)
