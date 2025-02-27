from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Рандомный факт')
    keyboard.button(text='Диалог с GPT')
    keyboard.button(text='Диалог с личностью')
    keyboard.button(text='QUIZ')
    keyboard.button(text='Помощь')
    keyboard.adjust(2, 3)
    return keyboard.as_markup(resize_keyboard=True)

def kb_random():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Хочу еще факт!')
    keyboard.button(text='Назад')
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)

def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Назад')
    return keyboard.as_markup(resize_keyboard=True)