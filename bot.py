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
        'quiz': quiz,
    }
    await actions.get(dialog.mode, start)(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /start тг бота """
    dialog.mode = 'main'
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓'
    })

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /random случайного факта из gpt """
    dialog.mode = 'random'
    text = load_message('random')
    await send_image(update, context, 'random')
    await send_text(update, context, text)
    msg = await send_text(update, context, 'Чат шевелит микросхемами...')
    prompt = load_prompt('random')
    answer = await chat_gpt.add_message(prompt)
    await msg.edit_text(answer)
    await send_text_buttons(update, context, 'Жжём дальше или хорош?', {'random_again': 'Хочу ещё факт', 'random_stop': 'Закончить'})

async def random_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик нажатия кнопок в случайном факте. Запрашиваем новый факт или выходим на стартовое меню """
    if update.callback_query.data == 'random_again':
        await random(update, context)
    else:
        await start(update, context)

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /gpt, тут мы общаемся с великим и могучим ИИ """
    print('gpt', update.message.text if update.message else 'no msg')
    dialog.mode = 'gpt'
    text = load_message('gpt')
    await send_image(update, context, 'gpt')
    await send_text(update, context, text)

async def gpt_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик сообщений в /gpt разделе чата """
    print('gpt_msg', update.message.text if update.message else 'no msg')
    msg = await send_text(update, context, 'Чат шевелит микросхемами...')
    prompt = load_prompt('gpt')
    answer = await chat_gpt.send_question(prompt, update.message.text)
    await msg.edit_text(answer)

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /talk """
    dialog.mode = 'talk'
    print('talk', update.message.text if update.message else 'no msg')

async def talk_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик сообщений в /talk разделе чата """
    print('talk_msg', update.message.text if update.message else 'no msg')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Обработчик команды /quiz """
    dialog.mode = 'quiz'
    print('quiz', update.message.text if update.message else 'no msg')

dialog = Dialog()
dialog.mode = 'start'

chat_gpt = ChatGptService(GPT_TOKEN)
app = ApplicationBuilder().token(TG_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_switcher))

# Зарегистрировать обработчик коллбэка можно так:
app.add_handler(CallbackQueryHandler(random_btn, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
