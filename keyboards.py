from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='ChatGPT')
    keyboard.button(text='Help')
    keyboard.button(text='LogOut')
    keyboard.adjust(2, 1)
    return keyboard.as_markup(resize_keyboard=True)

def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Назад')
    return keyboard.as_markup(resize_keyboard=True)