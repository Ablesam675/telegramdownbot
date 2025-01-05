from flask import Flask, request
from telebot import TeleBot, types
import os

# Initialize bot
BOT_TOKEN = "7700329167:AAE8jLLomrfDRQsr_lAjPovsB0XMxtaVOYs"
CHANNEL_LINK = "https://t.me/podzsphere"
bot = TeleBot(BOT_TOKEN)

# Flask app for webhook
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Handle /start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("Join Podz Sphere 🇵🇬", url=CHANNEL_LINK)
    markup.add(join_button)
    bot.send_message(
        message.chat.id,
        "Welcome! 🎉\n\nSend or forward any file, or upload a file to get a downloadable link. Also, click below to join our Telegram channel.",
        reply_markup=markup,
    )

# Handle file uploads
@bot.message_handler(content_types=["document", "photo", "video", "audio"])
def handle_files(message):
    try:
        file_id = ""
        file_type = ""

        if message.document:
            file_id = message.document.file_id
            file_type = "document"
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_type = "photo"
        elif message.video:
            file_id = message.video.file_id
            file_type = "video"
        elif message.audio:
            file_id = message.audio.file_id
            file_type = "audio"

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        bot.reply_to(
            message,
            f"Here is your {file_type} download link:\n{download_url}",
        )
    except Exception as e:
        bot.reply_to(message, "An error occurred while processing your file. Please try again.")

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    webhook_url = "https://telegramdownbot.onrender.com}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
