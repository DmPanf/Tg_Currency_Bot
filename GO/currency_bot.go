package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
)

const TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

type ValuteData struct {
	USD struct {
		Value float64 `json:"Value"`
	} `json:"USD"`
	EUR struct {
		Value float64 `json:"Value"`
	} `json:"EUR"`
	RUB struct {
		Value float64 `json:"Value"`
	} `json:"RUB"`
}

type CurrencyResponse struct {
	Valute ValuteData `json:"Valute"`
}

func getConversionRate(currency string) (float64, error) {
	resp, err := http.Get("https://www.cbr-xml-daily.ru/daily_json.js")
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	var cr CurrencyResponse
	err = json.Unmarshal(body, &cr)
	if err != nil {
		return 0, err
	}

	switch currency {
	case "USD":
		return cr.Valute.USD.Value, nil
	case "EUR":
		return cr.Valute.EUR.Value, nil
	case "RUB":
		return cr.Valute.RUB.Value, nil
	default:
		return 0, fmt.Errorf("Unknown currency: %s", currency)
	}
}

func main() {
	bot, err := tgbotapi.NewBotAPI(TOKEN)
	if err != nil {
		panic(err)
	}

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates, err := bot.GetUpdatesChan(u)
	if err != nil {
		panic(err)
	}

	for update := range updates {
		if update.Message == nil {
			continue
		}

		splitText := strings.Split(update.Message.Text, " ")
		if len(splitText) == 2 {
			currency := splitText[0]
			amount, err := strconv.ParseFloat(splitText[1], 64)
			if err == nil {
				rate, err := getConversionRate(currency)
				if err == nil {
					response := fmt.Sprintf("%f %s = %f RUB", amount, currency, amount*rate)
					msg := tgbotapi.NewMessage(update.Message.Chat.ID, response)
					bot.Send(msg)
				}
			}
		}
	}
}
