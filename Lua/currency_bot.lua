-- Install the lua-telegram-bot library using luarocks
-- luarocks install lua-telegram-bot

local telegram = require("telegram")
local http = require("socket.http")

local TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
local bot = telegram.bot(TOKEN)

local function convertCurrency(currencyCode, amount)
    local response = http.request("https://www.cbr-xml-daily.ru/daily_json.js")
    local data = json.decode(response)
    local rate = data["Valute"][currencyCode]["Value"]
    return amount * rate
end

bot.init()

bot.onText("^/start$", function(msg)
    bot.sendMessage(msg.chat.id, "Привет! Я бот для перевода валюты.\nДля использования отправьте сообщение в формате:\n<currency_code> <amount>\nНапример: USD 10")
end)

bot.onText("^(%u+)%s+(%d+)$", function(msg, matches)
    local currencyCode = matches[1]
    local amount = tonumber(matches[2])
    local result = convertCurrency(currencyCode, amount)
    bot.sendMessage(msg.chat.id, string.format("%s %s = %s RUB", amount, currencyCode, result))
end)

bot.run()
