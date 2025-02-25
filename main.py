import asyncio
from aiogram import Bot, Dispatcher

from config import TG_AIO_TOKEN
from handlers import router

def on_started():
    print('Bot started')

def on_stopped():
    print('Bot stopped')

async def start_bot():
    bot = Bot(token=TG_AIO_TOKEN)
    dispatch = Dispatcher()
    dispatch.startup.register(on_started)
    dispatch.shutdown.register(on_stopped)
    dispatch.include_routers(router)
    await dispatch.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print('Вах вах! Слюшай, что-то пошло не так!')