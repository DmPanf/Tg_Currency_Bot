# pip install pyTelegramBotAPI requests

import requests
import telebot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

def get_conversion_rate(currency):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()

    if currency in data['Valute']:
        return data['Valute'][currency]['Value']
    return None

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для перевода валюты.\nДля использования отправьте сообщение в формате:\n<currency_code> <amount>\nНапример: USD 10")

@bot.message_handler(regexp="^[A-Za-z]{3} \d+(\.\d+)?$")
def convert_currency(message):
    parts = message.text.split(' ')
    currency_code = parts[0].upper()
    amount = float(parts[1])
    
    rate = get_conversion_rate(currency_code)
    if rate:
        converted_value = rate * amount
        bot.reply_to(message, f"{amount} {currency_code} = {converted_value:.2f} RUB")
    else:
        bot.reply_to(message, f"Не удалось найти курс для {currency_code}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
