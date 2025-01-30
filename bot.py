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
    if dialog.mode == 'gpt':
        await start(update, context)
    elif dialog.mode == 'talk':
        await start(update, context)
    elif dialog.mode == 'quiz':
        await start(update, context)
    else:
        await start(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        # Добавить команду в меню можно так:
        # 'command': 'button text'
    })

async def random_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data == 'random_again':
        await random(update, context)
    else:
        await start(update, context)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'random'
    text = load_message('random')
    await send_image(update, context, 'random')
    await send_text(update, context, text)
    msg = await send_text(update, context, 'Чат шевелит микросхемами...')
    prompt = load_prompt('random')
    answer = await chat_gpt.add_message(prompt)
    await msg.edit_text(answer)
    await send_text_buttons(update, context, 'Жжём и ржём дальше?', {'random_again': 'Жги!', 'random_stop': 'Хорош'})

dialog = Dialog()
dialog.mode = None

chat_gpt = ChatGptService(GPT_TOKEN)
app = ApplicationBuilder().token(TG_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_switcher))

# Зарегистрировать обработчик коллбэка можно так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(random_btn, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
