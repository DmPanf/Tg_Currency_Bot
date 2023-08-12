import com.pengrad.telegrambot.TelegramBot;
import com.pengrad.telegrambot.UpdatesListener;
import com.pengrad.telegrambot.model.Update;
import com.pengrad.telegrambot.request.SendMessage;
import com.pengrad.telegrambot.response.SendResponse;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class CurrencyBot {
    public static final String TOKEN = "YOUR_TELEGRAM_BOT_TOKEN";

    public static void main(String[] args) {
        TelegramBot bot = new TelegramBot(TOKEN);
        bot.setUpdatesListener(updates -> {
            for (Update update : updates) {
                String messageText = update.message().text();
                String chatId = update.message().chat().id().toString();

                try {
                    String[] parts = messageText.split(" ");
                    String currencyCode = parts[0].toUpperCase();
                    double amount = Double.parseDouble(parts[1]);
                    double result = convertCurrency(currencyCode, amount);

                    String replyText = amount + " " + currencyCode + " = " + result + " RUB";
                    SendMessage request = new SendMessage(chatId, replyText);
                    SendResponse response = bot.execute(request);

                } catch (Exception e) {
                    bot.execute(new SendMessage(chatId, "Error occurred. Please use the correct format."));
                }
            }
            return UpdatesListener.CONFIRMED_UPDATES_ALL;
        });
    }

    private static double convertCurrency(String currencyCode, double amount) throws IOException {
        URL url = new URL("https://www.cbr-xml-daily.ru/daily_json.js");
        InputStream is = url.openStream();
        byte[] bytes = is.readAllBytes();
        String json = new String(bytes, StandardCharsets.UTF_8);

        JSONObject obj = new JSONObject(json);
        double rate = obj.getJSONObject("Valute").getJSONObject(currencyCode).getDouble("Value");
        return amount * rate;
    }
}
