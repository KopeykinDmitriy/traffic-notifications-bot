from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import time
import asyncio
import subprocess
import re
from datetime import datetime

def get_total_traffic():
    try:
        text = subprocess.run(["ifconfig eth0"], capture_output=True)
        matches = re.finditer('\(', text)
        indices = [match.start() for match in matches]
        index_first = indices[1]
        index_third = indices[2]
        matches = re.finditer('\)', text)
        indices = [match.start() for match in matches]
        index_second = indices[1]
        index_fourth = indices[2]
        received = f'Received: {text[index_first+1:index_second]}'
        transfered = f'Transfered: {text[index_third+1:index_fourth]}'
        return received + " " + transfered
    except Exception as err:
        return str(err)


ALLOWED_USER_ID = 000000000
API_TOKEN = 'Enter_Your_API_Token'
NOTIFICATION_PERIOD_SECONDS = 10

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
 
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
   if message.from_user.id == ALLOWED_USER_ID:
        await message.reply(f'Привет, {message.from_user.first_name}! Я твой новый бот.')
        while (True):
            await message.reply("[" + str(datetime.now()) + "] " + get_total_traffic())
            time.sleep(NOTIFICATION_PERIOD_SECONDS)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
