from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from requests import get

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def convert_currency(currency_code, amount=1):
    data = get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    rate = data['Valute'][currency_code]['Value']
    return round(amount * rate, 2)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    reply_text = ("Привет! Я бот для перевода валюты.\n"
                  "Для использования отправьте сообщение в формате:\n"
                  "<currency_code> <amount>\n"
                  "Например: USD 10")
    await message.reply(reply_text)

@dp.message_handler()
async def convert(message: types.Message):
    try:
        currency_code, amount = message.text.split()
        amount = float(amount)
        result = convert_currency(currency_code.upper(), amount)
        await message.reply(f"{amount} {currency_code.upper()} = {result} RUB")
    except Exception:
        await message.reply("Произошла ошибка. Убедитесь, что вы используете правильный формат.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
