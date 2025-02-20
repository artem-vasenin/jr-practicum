from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Рандомный факт')
    keyboard.button(text='Диалог с личностью')
    keyboard.button(text='Квиз')
    keyboard.button(text='Помощь')
    keyboard.adjust(2, 2)
    return keyboard.as_markup(resize_keyboard=True)

def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Назад')
    return keyboard.as_markup(resize_keyboard=True)