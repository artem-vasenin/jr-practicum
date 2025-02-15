import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, MessageHandler, ContextTypes, CommandHandler, filters

from gpt import ChatGptService
from util import (
    load_message,
    send_text,
    send_image,
    show_main_menu,
    default_callback_handler,
    send_text_buttons,
    load_prompt,
    Dialog
)


load_dotenv()
GPT_TOKEN = os.getenv("GPT_TOKEN")
TG_TOKEN = os.getenv("TG_TOKEN")


async def msg_switcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Роутер для перенаправления сообщений из чата в нужные обработчики сообщений """
    actions = {
        'gpt': gpt_msg,
        'talk': talk_msg,
        'quiz': quiz_msg,
        'translate': translate_msg,
    }
    await actions.get(dialog.mode, start)(update, context)


def clear_dialog():
    """ Очистка стейта """
    dialog.mode = 'start'
    dialog.lang = None
    dialog.quiz = None
    dialog.quiz_qty = [0, 0]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /start тг бота """
    clear_dialog()
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓',
        'translate': 'Перевести фразу 🇬🇧'
    })


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /random случайного факта из gpt """
    clear_dialog()
    dialog.mode = 'random'
    text = load_message('random')
    await send_image(update, context, 'random')
    msg = await send_text(update, context, text)
    prompt = load_prompt('random')
    answer = await chat_gpt.add_message(prompt)
    await msg.edit_text(answer)
    await send_text_buttons(update, context, 'Еще один факт?', {'random_gen': 'Хочу ещё факт', 'random_stop': 'Закончить'})


async def random_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в случайном факте. Запрашиваем новый факт или выходим на стартовое меню """
    if update.callback_query.data == 'random_gen':
        await random(update, context)
    else:
        await start(update, context)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /gpt, тут мы общаемся с великим и могучим ИИ """
    clear_dialog()
    dialog.mode = 'gpt'
    await send_image(update, context, 'gpt')
    await send_text(update, context, load_message('gpt'))
    chat_gpt.set_prompt(load_prompt('gpt'))


async def gpt_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик сообщений в /gpt разделе чата """
    msg = await send_text(update, context, 'Чат шевелит микросхемами...')
    try:
        answer = await chat_gpt.add_message(update.message.text)
        await msg.edit_text(answer)
    except Exception as e:
        print(e)
        await msg.edit_text('Ошибка. ЧатGPT слегка прилег...')


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /talk """
    clear_dialog()
    dialog.mode = 'talk'
    await send_image(update, context, 'talk')
    await send_text_buttons(update, context, load_message('talk'), {
        'talk_cobain': 'Курт Кобейн - Солист группы Nirvana 🎸',
        'talk_hawking': 'Стивен Хокинг - Физик 🔬',
        'talk_nietzsche': 'Фридрих Ницше - Философ 🧠',
        'talk_queen': 'Елизавета II - Королева Соединённого Королевства 👑',
        'talk_tolkien': 'Джон Толкиен - Автор книги "Властелин Колец" 📖',
    })


async def talk_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в разговоре с личностью. """
    btn_mode = update.callback_query.data
    await update.callback_query.answer()
    await send_image(update, context, btn_mode)
    chat_gpt.set_prompt(load_prompt(btn_mode))


async def talk_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик сообщений в /talk разделе чата """
    msg = await send_text(update, context, 'Собеседник впал в задумчивость...')
    try:
        answer = await chat_gpt.add_message(update.message.text)
        await msg.edit_text(answer)
    except Exception as e:
        print(e)
        await msg.edit_text('Ошибка. ЧатGPT слегка прилег...')


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /quiz """
    clear_dialog()
    dialog.mode = 'quiz'
    buttons = {
        'quiz_prog': 'Программирования на языке python',
        'quiz_math': 'Математическая теория',
        'quiz_biology': 'Биология',
    }
    await send_image(update, context, 'quiz')
    await send_text_buttons(update, context, load_message('quiz'), buttons)
    chat_gpt.set_prompt(load_prompt('quiz'))


async def quiz_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в викторине. """
    if update.callback_query.data == 'quiz_end':
        await start(update, context)
        return

    btn_mode = update.callback_query.data if not update.callback_query.data == 'quiz_more' else dialog.quiz
    dialog.quiz = btn_mode
    msg = await send_text(update, context, 'Что б такого спросить...')
    try:
        answer = await chat_gpt.add_message(btn_mode)
        await msg.edit_text(answer)
    except Exception as e:
        print(e)
        await msg.edit_text('Ошибка. ЧатGPT слегка прилег...')


async def quiz_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в викторине. """
    buttons = {
        'quiz_prog': 'Программирования на языке python',
        'quiz_math': 'Математическая теория',
        'quiz_biology': 'Биология',
    }
    answer = ''
    try:
        answer = await chat_gpt.add_message(update.message.text)
    except Exception as e:
        print(e)
        await send_text(update, context, 'Ошибка. ЧатGPT слегка прилег...')

    if answer == 'Правильно!':
        dialog.quiz_qty[0] += 1
    else:
        dialog.quiz_qty[1] += 1

    answer = answer + f'\nПравильных ответов: {dialog.quiz_qty[0]}, Неправильных: {dialog.quiz_qty[1]}'

    await send_text(update, context, answer)
    buttons['quiz_more'] = f'Повторить: {buttons[dialog.quiz]}'
    buttons['quiz_end'] = 'В главное меню'
    await send_text_buttons(update, context, 'Выбрать другую тему или повторить:', buttons)


async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /translate """
    clear_dialog()
    dialog.mode = 'translate'
    await send_image(update, context, 'translate')
    await send_text_buttons(update, context, load_message('translate'), {
        'translate_en': 'Русско-Английский переводчик 🇷🇺➡️🇬🇧',
        'translate_es': 'Русско-Испанский переводчик 🇷🇺➡️🇪🇸',
    })


async def translate_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в переводчике. """
    btn_mode = update.callback_query.data
    dialog.lang = btn_mode
    await send_text(update, context, load_message(btn_mode))


async def translate_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик сообщений переводчика """
    text = f'Переводчик с {"английского" if dialog.lang == "translate_en" else "испанского"} призадумался...'
    msg = await send_text(update, context, text)
    prompt = load_prompt(dialog.lang)
    answer = await chat_gpt.send_question(prompt, update.message.text)
    try:
        await msg.edit_text(answer)
    except Exception as e:
        print(e)
        await msg.edit_text('Ошибка. ЧатGPT слегка прилег...')


dialog = Dialog()
dialog.mode = 'start'
dialog.lang = None
dialog.quiz = None
dialog.quiz_qty = [0, 0]

chat_gpt = ChatGptService(GPT_TOKEN)
app = ApplicationBuilder().token(TG_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(CommandHandler('translate', translate))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_switcher))

app.add_handler(CallbackQueryHandler(random_btn, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(talk_btn, pattern='^talk_.*'))
app.add_handler(CallbackQueryHandler(quiz_btn, pattern='^quiz_.*'))
app.add_handler(CallbackQueryHandler(translate_btn, pattern='^translate_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
