import json
import data_preparation

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Read the secret data from env file
with open("env", "r") as f:
    secret = json.loads(f.read())
bot = Bot(token=secret['TG_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer(f"Hello, Enter /help")


@dp.message_handler(commands=['help'])
async def send_welcome(msg: types.Message):
    await msg.answer("""I can show you current BTCUSD and ETHUSD  relations \n
Just print BTCUSD or ETHUSD""")


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if 'btcusd' in msg.text.lower() and True:
        await msg.answer(f'{data_preparation.get_last_value("BTCUSD")}')
    elif 'ethusd' in msg.text.lower() and True:
        await msg.answer(f'{data_preparation.get_last_value("ETHUSD")}')
    else:
        await msg.answer("I am confused! Go back to /help")


if __name__ == '__main__':
    executor.start_polling(dp)
