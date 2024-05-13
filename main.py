import asyncio
import time

from aiogram import  Bot, Dispatcher
from app.function.function import remove_expired_users
from app.hendlers.hendlers import router



async def main():
    bot = Bot(token='5975408409:AAEDbY6RpKAu0hksILn3-tcNahw276EFg98')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    print("Бот працює")


    await remove_expired_users()


if  __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот відключен")
